from flask import Blueprint, render_template, request, redirect, url_for, abort, \
  flash, current_app
from server.data.display_row import DisplayRow
from server.services import display
from server.utils import random_uuid

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
  display.create_one(DisplayRow.from_request(request, random_uuid()))
  flash("Entry created successfully!", "success")
  return redirect(url_for("displays.index"), 303)


@bp.route("/edit/<int:pkey>", methods=["GET"])
def edit(pkey):
  validate_pkey(pkey)
  return render_template(
      "partials/displays/_edit.html.j2",
      display=display.find_one(pkey)
  )


@bp.route("/<int:pkey>", methods=["PUT"])
def update(pkey):
  validate_pkey(pkey)
  display.update_one(pkey, DisplayRow.from_request(request))
  flash("Entry updated successfully!", "success")
  return redirect(url_for("displays.index"), 303)


def validate_pkey(pkey):
  display_view = display.find_one(pkey)
  if display_view:
    return display_view
  else:
    flash("Display not found", "error")
    abort(404)
