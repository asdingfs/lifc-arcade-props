from flask import Blueprint, render_template, current_app, flash, request, \
  redirect, url_for
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
  return redirect(url_for("index"), 303)
