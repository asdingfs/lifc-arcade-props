from flask import Blueprint, current_app, abort, flash, make_response, request, \
  redirect, url_for
from server.services import badge_service, scan_service
from server.data.display_state import DisplayState

bp = Blueprint("scans", __name__, url_prefix="/scans")
app = current_app


@bp.route("/p1/<uuid>", methods=["POST"])
def new_p1(uuid):
  return new_input(uuid, True)


@bp.route("/p2/<uuid>", methods=["POST"])
def new_p2(uuid):
  return new_input(uuid, False)


@bp.route("/", methods=["POST"])
def create():
  uuid = request.form.get("code")
  player = request.form.get("player")
  p1_or_p2 = (player == "p1")
  new_input(uuid, p1_or_p2)
  return redirect(url_for("displays.index"), 303)


def new_input(code: str, p1_or_p2: bool):
  badge_record = badge_service.find_one_by_uuid(code)
  player = "p1" if p1_or_p2 else "p2"
  if badge_record:
    scan_record = scan_service.create_one(badge_record.pkey, p1_or_p2)
    if scan_record:
      # Update the display state with the new scan record
      state = DisplayState()  # singleton
      state.set_player(scan_record, player)
      display_view = state.generate()
      if display_view:
        flash(
            f"scanned ID for {player} successfully, and generated display!",
            "success"
        )
        return display_view
      else:
        return abort(
            500,
            f"failed to generate a post-scan display. "
            f"id: {scan_record.pkey}"
        )
    else:
      return abort(
          500, f"failed to create scan record for {player}"
      )
  else:
    return abort(
        404, f"badge with {code} not found"
    )
