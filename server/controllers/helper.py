from flask import flash, abort
from server.utils import allowed_file

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