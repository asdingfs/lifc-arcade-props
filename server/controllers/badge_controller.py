from flask import Blueprint, render_template, current_app, flash, request, \
  redirect, url_for, abort
from server.services import badge_service
from server.data.badge_record import BadgeRecord
import urllib.parse

bp = Blueprint("badges", __name__, url_prefix="/badges")
app = current_app


@bp.route("/", methods=["GET"])
def index():
  search = request.args.get("search", None)
  page = request.args.get("page", 0, type=int)
  size = request.args.get("size", 20, type=int)
  return render_template(
      "partials/badges/_index.html.j2",
      records=badge_service.find_all(search, page, size),
      enc_search=urllib.parse.quote_plus(search) if search else None,
      page=page, size=size,
  )


@bp.route("/new", methods=["GET"])
def new():
  return render_template("partials/badges/_new.html.j2")


@bp.route("/", methods=["POST"])
def create():
  badge_service.create_one(BadgeRecord.from_request(request))
  flash("Entry created successfully!", "success")
  return redirect(url_for("index", page="players"), 303)


@bp.route("/edit/<int:pkey>", methods=["GET"])
def edit(pkey):
  validate_pkey(pkey)
  return render_template(
      "partials/badges/_edit.html.j2",
      badge=badge_service.find_one(pkey)
  )


@bp.route("/<int:pkey>", methods=["PUT"])
def update(pkey):
  validate_pkey(pkey)
  badge_service.update_one(pkey, BadgeRecord.from_request(request))
  flash("Entry updated successfully!", "success")
  return redirect(url_for("index", page="players"), 303)


@bp.route("/<int:pkey>", methods=["DELETE"])
def delete(pkey):
  validate_pkey(pkey)
  badge_service.delete_one(pkey)
  flash("Entry deleted successfully!", "success")
  return redirect(url_for("index", page="players"), 303)


def validate_pkey(pkey):
  record = badge_service.find_one(pkey)
  if record:
    return record
  else:
    flash("Badge not found", "error")
    abort(404)
