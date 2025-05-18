import os
from flask import Flask, render_template
from . import db, constants
from server.controllers import display_controller, media_controller
from server.constants import DATABASE_NAME, UPLOAD_FOLDER


def create_app(test_config=None):
  # create and configure the app
  app = Flask(
      __name__,
      instance_relative_config=True,
      template_folder="templates",
  )

  app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, DATABASE_NAME),
      UPLOAD_FOLDER=os.path.join(
          app.static_folder, UPLOAD_FOLDER
      )
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # setup database
  db.init_app(app)

  # root page declarations
  @app.route("/")
  def index():
    return render_template("index.html.j2")

  # register blueprints
  app.register_blueprint(display_controller.bp)
  app.register_blueprint(media_controller.bp)

  return app
