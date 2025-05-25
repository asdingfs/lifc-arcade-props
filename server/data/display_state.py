from flask import current_app
from copy import deepcopy
from server.data.scan_record import ScanRecord
from server.data.display_record import DisplayRecord
from server.data.display_view import DisplayView
from server.services import badge_service, display_service, media_service, \
  random_service, pixel_service
from server.utils import random_uuid
import threading

config_lock = threading.Lock()
app = current_app


def get_default():
  return {
    "p1": None, "p2": None, "display_id": None,
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


def default_player_set():
  badge = badge_service.find_one_random_default()
  return player_set(badge.pkey if badge else None)


class DisplayState:
  _instance = None
  _state = deepcopy(get_default())
  _lock = threading.Lock()

  def __new__(cls):
    if cls._instance is None:
      with cls._lock:
        # Another thread could have created the instance
        # before we acquired the lock. So check that the
        # instance is still non-existent.
        if not cls._instance:
          cls._instance = super().__new__(cls)
    return cls._instance

  def get(self):
    with self._lock:
      return deepcopy(self._state)

  def set_player(self, new_record: ScanRecord | None, key: str):
    state = self.get()
    with self._lock:
      old_record = state.get(key, None)
      if getattr(old_record, "pkey", None) == getattr(new_record, "pkey", None):
        return self._state
      else:
        state[key] = new_record
        state["changed_players"] = True
        self._state = state
        return state

  def set_display(self, new_display: DisplayView | None):
    state = self.get()
    with self._lock:
      old_display = state.get("display_id", None)
      if getattr(old_display, "pkey", None) == getattr(
          new_display, "pkey", None
      ):
        return self._state
      else:
        state["display_id"] = new_display.pkey if new_display else None
        state["changed_display"] = True
        self._state = state
        return state

  def generate(self):
    state = self.get()
    with self._lock:
      p1_set = player_set(
          getattr(state["p1"], "badge_id", None)
      ) or default_player_set()
      p2_set = player_set(
          getattr(state["p2"], "badge_id", None)
      ) or default_player_set()
      if p1_set and p2_set:
        record = DisplayRecord(*p1_set, *p2_set, random_uuid())
        display_view = display_service.create_one(record)
        state["display_id"] = display_view.pkey
        state["changed_display"] = True
        self._state = state
        return display_view
      else:
        return None

  def changed(self):
    state = self.get()
    with self._lock:
      state["changed_players"] = False
      state["changed_display"] = False
      self._state = state

  def sync(self):
    """Synchronize the display state with the current configuration."""
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

  def sync_display(self, display):
    if display:
      pixel_service.push(display)
      self.changed()
      return display
    else:
      return None
