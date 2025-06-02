#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python

from constants import RESET_BUTTON_PIN_IN, RESET_LED_PIN_OUT
from arcade_button import press, listen
from apis import display_reset
import RPi.GPIO as GPIO
import logging

# setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RESET_BUTTON_PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RESET_LED_PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='reset_button.log',  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)

# avoid spamming by waiting for 2 second before next button press will be registered
# in contrast, the LED will flash when the button is pressed for 1s
logger.info("starting reset button listener...")
try:
  while True:
    listen(
        RESET_BUTTON_PIN_IN,
        on_press=lambda: press(logger, display_reset, RESET_LED_PIN_OUT),
        logger=logger,
    )
finally:
  GPIO.cleanup()
