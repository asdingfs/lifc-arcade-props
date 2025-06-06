import os
from flask import Flask, render_template, request
from flask.logging import default_handler
from . import db, constants
from server.services import scheduler_service, pixel_service
from server.constants import DATABASE_NAME, UPLOAD_FOLDER
from server.config.ap_scheduler_config import APSchedulerConfig
from server.config.logger_config import LoggerFormatter
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS


def create_app(test_config=None):
  # Get env file path from environment variable, default to .env
  env_path = os.getenv('FLASK_ENV_FILE', '.env')
  load_dotenv(env_path)
  # create and configure the app
  app = Flask(
      __name__,
      instance_relative_config=True,
      template_folder="templates",
  )
  app.config.from_object(APSchedulerConfig())
  app.config.update(
      # Environment-specific configuration
      SECRET_KEY=os.getenv("SECRET_KEY", 'dev'),
      SERVER_NAME=os.getenv("SERVER_NAME", 'Lifc2025PropsServer.local'),
      PREFERRED_URL_SCHEME=os.getenv('PREFERRED_URL_SCHEME', 'http'),
      APPLICATION_ROOT=os.getenv('APPLICATION_ROOT', '/'),
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

  # setup default logging
  default_handler.setFormatter(LoggerFormatter.default())

  # root page declarations
  @app.route("/")
  def home():
    return render_template("index.html.j2")

  @app.route("/app", methods=["GET"])
  def index():
    search = request.args.get("search", None)
    page = request.args.get("page", 0, type=int)
    size = request.args.get("size", 20, type=int)
    return render_template(
        "app.html.j2",
        search=search, page=page, size=size,
    )

  # setup database
  db.init_app(app)

  # setup scheduler
  scheduler = scheduler_service.get_scheduler()
  scheduler.init_app(app)

  # setup reverse proxy (nginx)
  app.wsgi_app = ProxyFix(
      app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
  )

  # setup cors
  CORS(
      app,
      resources={
        r"/*": {
          "origins": f"http://{app.config['SERVER_NAME']}"
        }
      }
  )

  with app.app_context():
    # load tasks and start scheduler
    from server.tasks import display_tasks
    scheduler.start()

    # register blueprints
    from server.controllers import display_controller, media_controller, \
      score_controller, input_controller
    app.register_blueprint(display_controller.bp)
    app.register_blueprint(media_controller.bp)
    app.register_blueprint(score_controller.bp)
    app.register_blueprint(input_controller.bp)

    app.logger.info("flask initialized successfully!")
    return app
