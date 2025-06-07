from typing import Callable, Any
from flask import Blueprint, current_app, abort, flash, make_response, request, \
  redirect, url_for
from server.services import badge_service, scan_service
from server.data.display_state import DisplayState

bp = Blueprint("inputs", __name__, url_prefix="/inputs")
app = current_app


@bp.route("/p1/<uuid>", methods=["POST"])
def new_p1(uuid):
  return new_input(
      uuid, True,
      on_success=lambda: make_response("", 204)
  )


@bp.route("/p2/<uuid>", methods=["POST"])
def new_p2(uuid):
  return new_input(
      uuid, False,
      on_success=lambda: make_response("", 204)
  )


@bp.route("/sync", methods=["POST"])
def sync():
  DisplayState().sync()
  return make_response("", 204)


@bp.route("/reset", methods=["POST"])
def reset():
  DisplayState().regress(force=True)
  return make_response("", 204)


@bp.route("/", methods=["POST"])
def create():
  uuid = request.form.get("code")
  player = request.form.get("player")
  if player is None:
    return abort(400, "player must be specified")
  else:
    p1_or_p2 = (player == "p1")
  return new_input(
      uuid, p1_or_p2,
      on_success=lambda: redirect(url_for("pages.displays"), 303)
  )


def new_input(code: str, p1_or_p2: bool, on_success: Callable[[], Any]):
  badge_record = badge_service.find_one_by_uuid(code)
  player = "p1_id" if p1_or_p2 else "p2_id"
  if badge_record:
    scan_record = scan_service.create_one(badge_record.pkey, p1_or_p2)
    if scan_record:
      # Update the display state with the new scan record
      state = DisplayState()  # singleton
      state.set_player(scan_record, player)
      flash(
          f"scanned ID for {player} successfully!",
          "success"
      )
      return on_success()
    else:
      return abort(
          500, f"failed to create scan record for {player}"
      )
  else:
    return abort(
        404, f"badge with {code} not found"
    )
