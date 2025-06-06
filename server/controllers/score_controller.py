from flask import Blueprint, render_template, redirect, url_for, current_app
from server.services import display_service

bp = Blueprint("scores", __name__, url_prefix="/scores")
app = current_app


@bp.route("/top", methods=["GET"])
def top():
  return render_template(
      "partials/displays/_top_score.html.j2",
      top_score=display_service.top_score(),
  )


@bp.route("/", methods=["DELETE"])
def reset():
  display_service.reset_scores()
  return redirect(url_for("index", page="displays"), 303)
