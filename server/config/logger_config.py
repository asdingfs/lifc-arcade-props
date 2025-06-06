from flask import has_request_context, request
import logging


class LoggerFormatter(logging.Formatter):
  def format(self, record):
    if has_request_context():
      record.url = request.url
      record.remote_addr = request.remote_addr
    else:
      record.url = None
      record.remote_addr = None

    return super().format(record)

  @classmethod
  def default(cls):
    return LoggerFormatter(
        "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s"
    )

  @classmethod
  def request(cls):
    return LoggerFormatter(
        '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s '
        '(Request: %(remote_addr)s requested %(url)s in %(module)s)'
    )
