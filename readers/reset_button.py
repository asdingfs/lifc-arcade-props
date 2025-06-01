#!/home/trigger/lifc-arcade-props/readers/.venv/bin/python

from RPi.GPIO import GPIO
from constants import RESET_BUTTON_PIN_IN, RESET_LED_PIN_OUT, SERVER_URL
import time
import requests
import logging

# setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RESET_BUTTON_PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RESET_LED_PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='sync_button.log',  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)

# avoid spamming by waiting for 2 second before next button press will be registered
# in contrast, the LED will flash when the button is pressed for 1s
logging.info("starting reset button listener...")
while True:
  if GPIO.input(RESET_BUTTON_PIN_IN) == GPIO.HIGH:
    logging.info("reset button pressed! sending reset request to server...")
    # execute the sync display from API
    response = requests.post(f"{SERVER_URL}/displays/reset")
    if response.status_code == 204:
      # will flash the LED once
      logging.info("display reset request sent successfully!")
      GPIO.output(RESET_LED_PIN_OUT, GPIO.LOW)
      time.sleep(1)
      GPIO.output(RESET_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(1)
    else:
      # will flash the LED 3 times
      logging.error(
          f"failed to send display reset request, status: {response.status_code}",
      )
      GPIO.output(RESET_LED_PIN_OUT, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(RESET_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(RESET_LED_PIN_OUT, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(RESET_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(RESET_LED_PIN_OUT, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(RESET_LED_PIN_OUT, GPIO.HIGH)
      time.sleep(0.5)
