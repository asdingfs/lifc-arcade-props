#!/home/trigger/lifc-arcade-props/readers/.venv/bin/python

from RPi.GPIO import GPIO
from constants import SYNC_BUTTON_PIN_IN, SYNC_LED_PIN_OUT, SERVER_URL
import time
import requests
import logging

# setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SYNC_BUTTON_PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SYNC_LED_PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='sync_button.log',  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)

# avoid spamming by waiting for 2 second before next button press will be registered
# in contrast, the LED will flash when the button is pressed for 1s
logging.info("starting sync button listener...")
while True:
  if GPIO.input(SYNC_BUTTON_PIN_IN) == GPIO.HIGH:
    logging.info("start button pressed! sending sync request to server...")
    # execute the sync display from API
    response = requests.post(f"{SERVER_URL}/displays/sync")
    if response.status_code == 204:
      # will flash the LED once
      logging.info("display sync request sent successfully!")
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.LOW)
      time.sleep(1)
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(1)
    else:
      # will flash the LED 3 times
      logging.error(
          f"failed to send display sync request, status: {response.status_code}",
      )
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(SYNC_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(0.5)
