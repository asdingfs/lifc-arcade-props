# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from server import create_app
from server.data.display_state import DisplayState
from server.config.logger_config import LoggerFormatter
import logging

application = create_app()

if __name__ != "__main__":
  # setup logging from gunicorn
  gunicorn_logger = logging.getLogger('gunicorn.error')
  if gunicorn_logger.handlers:
    for handler in gunicorn_logger.handlers:
      handler.setFormatter(LoggerFormatter.request())
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)
  else:
    pass  # use default logging


def server():
  application.run()


def init():
  with application.app_context():
    application.logger.info("syncing display now!")
    DisplayState().sync()  # Ensure the display state is synced on startup


init()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  server()
