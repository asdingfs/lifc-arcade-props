from flask import Blueprint, request, current_app, render_template
from server.controllers import helper
from server.services import media

bp = Blueprint("media", __name__, url_prefix="/media")
app = current_app


# returns ID only
@bp.route("/upload", methods=["POST"])
def create():
  input_name = request.form.get("inputName")
  output_id = request.form.get("outputId")
  output_name = request.form.get("outputName")
  valid_file = helper.validate_file(request.files.get(input_name))
  created_id = media.create_one(valid_file)
  return render_template(
      "partials/media/_id_input.html.j2",
      id=output_id,
      name=output_name,
      value=created_id,
  )
