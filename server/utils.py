from flask import current_app, url_for
from server.constants import ALLOWED_EXTENSIONS
import os


def allowed_file(filename):
  return (
      '.' in filename
      and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  )


def uploaded_file_fullpath(filename):
  return os.path.join(
      current_app.config['UPLOAD_FOLDER'], filename
  )


def uploaded_file_path(filename):
  relative_folder = current_app.config['UPLOAD_FOLDER'].replace(
      f"{current_app.static_folder}/", '', 1
  )
  return url_for(
      'static',
      filename=os.path.join(relative_folder, filename)
  )
