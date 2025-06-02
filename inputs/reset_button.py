#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python

from constants import RESET_BUTTON_PIN_IN, RESET_LED_PIN_OUT
from arcade_button import press, listen
from apis import display_reset
import RPi.GPIO as GPIO
import logging
import os

# setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RESET_BUTTON_PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RESET_LED_PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)

# setup logging
script_dir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(script_dir, 'buttons.log'),
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# avoid spamming by waiting for 2 second before next button press will be registered
# in contrast, the LED will flash when the button is pressed for 1s
logger.info("starting reset button listener...")
try:
  while True:
    listen(
        RESET_BUTTON_PIN_IN,
        on_press=lambda: press(
            logger, display_reset, RESET_LED_PIN_OUT, "reset"
        ),
        logger=logger,
    )
finally:
  GPIO.cleanup()
