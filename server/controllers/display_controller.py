from flask import Blueprint, render_template, request, redirect, url_for, abort, \
  flash, current_app, make_response, send_file
from server.data.display_state import DisplayState
from server.data.display_record import DisplayRecord
from server.services import display_service, pixel_service
from server.utils import random_uuid
import urllib.parse

bp = Blueprint("displays", __name__, url_prefix="/displays")
app = current_app


@bp.route("/", methods=["GET"])
def index():
  search = request.args.get("search", None)
  page = request.args.get("page", 0, type=int)
  size = request.args.get("size", 20, type=int)
  return render_template(
      "partials/displays/_index.html.j2",
      records=display_service.find_all(search, page, size),
      enc_search=urllib.parse.quote_plus(search) if search else None,
      page=page, size=size,
  )


@bp.route("/<int:pkey>", methods=["GET"])
def show(pkey):
  validate_pkey(pkey)
  display = display_service.find_one(pkey)
  DisplayState().set_display(display)
  if pixel_service.push(display):
    flash("Display pushed successfully!", "success")
    return make_response("", 204)
  else:
    abort(
        500,
        "Pushing pixels failed! Please check logs for more information."
    )


@bp.route("/download/<int:pkey>", methods=["GET"])
def download(pkey):
  validate_pkey(pkey)
  display = display_service.find_one(pkey)
  (filepath, filename, mimetype) = pixel_service.download(display)
  if filepath:
    return send_file(
        filepath,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename,
    )
  else:
    flash("Preview generation failed!", "error")
    return abort(500, message="unknown error when generating preview")


@bp.route("/sync", methods=["POST"])
def sync():
  DisplayState().sync()
  flash("All displays synced successfully!", "success")
  return redirect(url_for("index", page="displays"), 303)


@bp.route("/create", methods=["GET"])
def new():
  return render_template("partials/displays/_new.html.j2")


@bp.route("/", methods=["POST"])
def create():
  display_service.create_one(DisplayRecord.from_request(request, random_uuid()))
  flash("Entry created successfully!", "success")
  return redirect(url_for("index", page="displays"), 303)


@bp.route("/edit/<int:pkey>", methods=["GET"])
def edit(pkey):
  validate_pkey(pkey)
  return render_template(
      "partials/displays/_edit.html.j2",
      display=display_service.find_one(pkey)
  )


@bp.route("/<int:pkey>", methods=["PUT"])
def update(pkey):
  validate_pkey(pkey)
  display_service.update_one(pkey, DisplayRecord.from_request(request))
  flash("Entry updated successfully!", "success")
  return redirect(url_for("index", page="displays"), 303)


@bp.route("/<int:pkey>", methods=["DELETE"])
def delete(pkey):
  validate_pkey(pkey)
  display_service.delete_one(pkey)
  flash("Entry deleted successfully!", "success")
  return redirect(url_for("index", page="displays"), 303)


def validate_pkey(pkey):
  display_view = display_service.find_one(pkey)
  if display_view:
    return display_view
  else:
    flash("Display not found", "error")
    abort(404)
