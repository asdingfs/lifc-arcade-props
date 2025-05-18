from flask import Blueprint, render_template, request, redirect, url_for, abort, \
  flash, current_app
from server.data.display_row import DisplayRow
from server.services import display

bp = Blueprint("displays", __name__, url_prefix="/displays")
app = current_app


@bp.route("/", methods=["GET"])
def index():
  return render_template(
      "partials/displays/_index.html.j2",
      entries=display.find_all(),
  )


@bp.route("/create", methods=["GET"])
def new():
  return render_template("partials/displays/_new.html.j2")


@bp.route("/", methods=["POST"])
def create():
  p1_media_id = request.form.get("p1_media_id", type=int)
  p2_media_id = request.form.get("p2_media_id", type=int)
  display_row = DisplayRow.from_request(request, p1_media_id, p2_media_id)
  display.create_one(display_row)
  flash("Entry created successfully!", "success")
  return redirect(url_for("displays.index"))


@bp.route("/edit/<int:pkey>", methods=["GET"])
def edit(pkey):
  return render_template(
      "partials/displays/_edit.html.j2",
      display=display.find_one(pkey)
  )


def validate_pkey(pkey):
  display_view = display.find_one(pkey)
  if display_view:
    return display_view
  else:
    flash("Display not found", "error")
    abort(404)
