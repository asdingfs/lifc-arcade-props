from flask import flash, abort
from server.utils import allowed_file
from werkzeug.datastructures import FileStorage


def validate_file(file: FileStorage):
  if file:
    if allowed_file(file.filename):
      return file
    else:
      flash("Invalid file type. Please upload an image.", "error")
      abort(422)
  else:
    flash("No file provided", "error")
    abort(422)
