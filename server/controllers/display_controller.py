from flask import Blueprint, render_template, request, redirect, url_for, abort, \
  flash, current_app
from server.utils import allowed_file
from server.data.display_row import DisplayRow
from server.services.display import find_all, find_one, create_one
from server.services.media import create_players_media
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import sqlite3

bp = Blueprint("displays", __name__, url_prefix="/displays")
app = current_app


@bp.route("/", methods=["GET"])
def index():
  return render_template(
      "partials/displays/_index.html.j2",
      entries=find_all(),
  )


@bp.route("/", methods=["POST"])
def create():
  p1_file = validate_file(request.files.get("p1_file"))
  p2_file = validate_file(request.files.get("p2_file"))
  (p1_media_id, p2_media_id) = create_players_media(p1_file, p2_file)
  display_row = DisplayRow.from_request(request, p1_media_id, p2_media_id)
  create_one(display_row)
  flash("Entry created successfully!", "success")
  return redirect(url_for("displays.index"))


@bp.route("/create", methods=["GET"])
def new():
  return render_template("partials/displays/_new.html.j2")


def validate_pkey(pkey):
  display_view = find_one(pkey)
  if display_view:
    return display_view
  else:
    flash("Display not found", "error")
    abort(404)


def validate_file(file):
  if file:
    if allowed_file(file.filename):
      return file
    else:
      flash("Invalid file type. Please upload an image.", "error")
      abort(422)
  else:
    flash("No file provided", "error")
    abort(422)
