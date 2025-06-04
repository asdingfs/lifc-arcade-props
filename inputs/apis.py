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
    if 200 <= response.status_code < 300:
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
  return call_request(
      lambda: requests.post(
          f"{SERVER_URL}/inputs/sync",
          timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
      ),
      logger,
      "inputs sync",
  )


def display_reset(logger):
  """
  Reset the display by sending a request to the server.
  This function is called when the reset button is pressed.
  It will send a request to the server to reset the display.
  """
  return call_request(
      lambda: requests.post(
          f"{SERVER_URL}/inputs/reset",
          timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
      ),
      logger,
      "inputs reset",
  )


def register_p1(p1_uid, logger):
  """
  Register the P1 UID from RFID reader.
  """
  return call_request(
      lambda: requests.post(
          f"{SERVER_URL}/inputs/p1/{p1_uid}",
          timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
      ),
      logger,
      "register p1"
  )


def register_p2(logger, p2_uid):
  """
  Register the P1 UID from RFID reader.
  """
  return call_request(
      lambda: requests.post(
          f"{SERVER_URL}/inputs/p2/{p2_uid}",
          timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
      ),
      logger,
      "register p2"
  )
