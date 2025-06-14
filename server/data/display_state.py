from flask import current_app
from server.data.scan_record import ScanRecord
from server.data.display_record import DisplayRecord
from server.data.display_view import DisplayView
from server.services import badge_service, display_service, media_service, \
  random_service, pixel_service, redis_service, scan_service
from server.utils import random_uuid
import os
import threading

config_lock = threading.Lock()
app = current_app


def get_default():
  return {
    # renamed "p1" to "p1_id" and "p2" to "p2_id", as it's easier to save on redis
    "p1_id": None, "p2_id": None, "display_id": None,
    "changed_players": True, "changed_display": True
  }


# player set is defined as (name, media_id, score)
def player_set(badge_id: int | None):
  badge = badge_service.find_one(badge_id) if badge_id else None
  if badge:
    score = random_service.random_score()
    media_id = badge.media_id
    if not media_id:
      media_id = getattr(media_service.find_one_random_sample(), "pkey", None)
    return badge.name, media_id, score
  else:
    return None


def default_player_set(n: int = 1):
  badges = badge_service.find_random_defaults(n)
  return [player_set(badge.pkey if badge else None) for badge in badges]


class DisplayState:
  _instance = None
  _redis_key = "app:display_state"
  _redis = redis_service.get_instance()
  _lock = threading.Lock()

  def __new__(cls):
    cls.log_with_pid(
        "DisplayState instance requested (__new__)...",
        True
    )
    if cls._instance is None:
      with cls._lock:
        # Another thread could have created the instance
        # before we acquired the lock. So check that the
        # instance is still non-existent.
        if not cls._instance:
          cls._instance = super().__new__(cls)
          cls._instance.init_state()
    return cls._instance

  def init_state(self):
    """Initialize the display state from Redis or set to default."""
    self.log_with_pid(
        "Setting defaults for DisplayState (init_state)...",
        True
    )
    self._redis.set_json_dict(self._redis_key, get_default())

  def get(self):
    """Get the current display state from Redis."""
    self.log_with_pid(
        "Getting DisplayState from redis (get)...",
        True
    )
    return self._redis.get_json_dict(self._redis_key)

  def set_player(self, new_record: ScanRecord | None, key: str):
    self.log_with_pid(
        "Setting player to DisplayState (set_player)...",
        True
    )
    state = self.get()
    old_id = state.get(key, None)
    old_record = badge_service.find_one(old_id) if old_id else None
    with self._lock:
      if getattr(old_record, "pkey", None) == getattr(new_record, "pkey", None):
        # i.e. no need to change
        return state
      else:
        state[key] = new_record.pkey if new_record else None
        state["changed_players"] = True
        self._redis.set_json_dict(self._redis_key, state)
        return state

  def set_display(self, new_display: DisplayView | None):
    self.log_with_pid(
        "Setting a new display_id to show (set_display)...",
        True
    )
    state = self.get()
    with self._lock:
      old_display_id = state.get("display_id", None)
      if old_display_id == getattr(new_display, "pkey", None):
        return state  # no changes to state
      else:
        state["display_id"] = new_display.pkey if new_display else None
        state["changed_display"] = True
        self._redis.set_json_dict(self._redis_key, state)
        return state

  def generate(self):
    state = self.get()
    (p1_default, p2_default) = default_player_set(2)
    # fetch scan record -> badge_id & obtain player_set
    p1_id, p2_id = state.get("p1_id", None), state.get("p2_id", None)
    self.log_with_pid(
        f"Generating a display record (generate) "
        f"for P1: {p1_id} & P2: {p2_id}..."
    )
    p1_scan_record = scan_service.find_one(p1_id) if p1_id else None
    p2_scan_record = scan_service.find_one(p2_id) if p2_id else None
    with self._lock:
      p1_set = player_set(
          getattr(p1_scan_record, "badge_id", None)
      ) or p1_default
      p2_set = player_set(
          getattr(p2_scan_record, "badge_id", None)
      ) or p2_default
      if p1_set and p2_set:
        record = DisplayRecord(*p1_set, *p2_set, random_uuid())
        display_view = display_service.create_one(record)
        state["display_id"] = display_view.pkey
        state["changed_display"] = True
        self._redis.set_json_dict(self._redis_key, state)
        return display_view
      else:
        return None

  def after_change(self):
    state = self.get()
    with self._lock:
      state["changed_players"] = False
      state["changed_display"] = False
      self._redis.set_json_dict(self._redis_key, state)

  # will always regress if force is set to True
  def regress(self, force: bool = False):
    """Reset the display state to default."""
    force and self.log_with_pid("forcing display state to regress...")
    state = self.get()
    p1_id, p2_id = state.get("p1_id", None), state.get("p2_id", None)
    p1_scan_record = scan_service.find_one(p1_id) if p1_id else None
    p2_scan_record = scan_service.find_one(p2_id) if p2_id else None
    changed = False
    with self._lock:
      if p1_scan_record and (p1_scan_record.is_inactive() or force):
        p1_scan_record.is_inactive() and self.log_with_pid(
            "p1_scan_record is inactive, nullify state..."
        )
        changed = True
        state["p1_id"] = None
      if p2_scan_record and (p2_scan_record.is_inactive() or force):
        p2_scan_record.is_inactive() and self.log_with_pid(
            "p2_scan_record is inactive, nullify state..."
        )
        changed = True
        state["p2_id"] = None
      if changed:
        state["changed_players"] = True
      self._redis.set_json_dict(self._redis_key, state)
    # after changing state, sync the display if
    #     display is changed as a result of regress() method
    if changed:
      # force is set to True or there are inactive players, regressing display...
      return self.sync()
    else:
      return None

  def sync(self):
    """Synchronize the display state with the current configuration."""
    self.log_with_pid(
        "Synchronizing display state (sync)...",
        True
    )
    state = self.get()  # to avoid mutilations by other processes
    changed_players = state.get("changed_players", None)
    changed_display = state.get("changed_display", None)
    if changed_players:
      return self.sync_players()
    elif changed_display:
      # If display_id is set, fetch the display from the service
      display_id = state["display_id"]
      if display_id:  # if set use the display to set the ID
        display = display_service.find_one(display_id)
        return self.sync_display(display)
      else:
        return self.sync_players()  # if unset, fetch from player and generate display
    else:
      return None

  def sync_players(self):
    return self.sync_display(self.generate())

  # TODO: IDEA: during sync_display, add time, so we know when is was last displayed
  def sync_display(self, display):
    self.log_with_pid("pushing pixels to led panels...")
    if display:
      pixel_service.push(display)
      self.after_change()
      return display
    else:
      return None

  @classmethod
  def log_with_pid(cls, message: str, debug: bool = False):
    """Log the current process ID for debugging purposes."""
    pid = os.getpid()
    msg = f"[PID #{pid}] {message}"
    app.logger.debug(msg) if debug else app.logger.info(msg)
