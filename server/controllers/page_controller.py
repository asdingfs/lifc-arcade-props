from flask import Blueprint, render_template, redirect, url_for, current_app

bp = Blueprint("pages", __name__, url_prefix="/pages")
app = current_app


@bp.route("/displays", methods=["GET"])
def displays():
  return render_template(
      "partials/pages/_displays.html.j2",
  )

@bp.route("/players", methods=["GET"])
def players():
  return render_template(
      "partials/pages/_players.html.j2",
  )