from constants import SERVER_URL, CONNECT_TIMEOUT, READ_TIMEOUT
import requests


def describe_request_description(desc=None):
  """
  Decorator to add a description to a function.
  This can be used to provide additional context or information about the function.
  """
  return f"{desc} request".capitalize() if desc else f"request".capitalize()


def call_request(call, logger, desc=None):
  this = describe_request_description(desc)
  try:
    response = call()
    if response.status_code >= 200:
      logger.info(f"{this} successful!")
      return True
    else:
      logger.error(
          f"{this} failed "
          f"with status code: {response.status_code}"
      )
      return False
  except IOError as e:
    logger.error(f"IOError during {this}: {str(e)}")
    return False


def display_sync(logger):
  """
  Sync the display by sending a request to the server.
  This function is called when the sync button is pressed.
  It will send a request to the server to sync the display.
  """
  call_request(
      lambda: requests.post(
          f"{SERVER_URL}/displays/sync",
          timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
      ),
      logger,
      "display sync",
  )


def display_reset(logger):
  """
  Reset the display by sending a request to the server.
  This function is called when the reset button is pressed.
  It will send a request to the server to reset the display.
  """
  call_request(
      lambda: requests.post(
          f"{SERVER_URL}/displays/reset",
          timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
      ),
      logger,
      "Display reset",
  )
