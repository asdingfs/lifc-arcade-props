from flask import Blueprint, request, current_app, render_template, flash, abort
from server.controllers import helper
from server.services import media_service

bp = Blueprint("media", __name__, url_prefix="/media")
app = current_app


@bp.route("/upload", methods=["POST"])
def create():
  input_file = request.form.get("inputFile")
  valid_file = helper.validate_file(request.files.get(input_file))
  record = media_service.create_one(valid_file)
  return render_template(
      "partials/media/_input_preview.html.j2",
      name=request.form.get("outputName"),
      record=record,
  )


@bp.route("/<int:pkey>", methods=["GET"])
def show(pkey):
  record = validate_pkey(pkey)
  return render_template(
      "partials/media/_input_preview.html.j2",
      name=request.args.get("outputName"),
      record=record,
  )


def validate_pkey(pkey):
  record = media_service.find_one(pkey)
  if record:
    return record
  else:
    flash("Display not found", "error")
    abort(404)
