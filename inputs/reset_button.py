#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python

from constants import RESET_BUTTON_PIN_IN, RESET_LED_PIN_OUT
from arcade_button import press, listen
from apis import display_reset
import RPi.GPIO as GPIO
import logging
import os
import subprocess

# setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RESET_BUTTON_PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RESET_LED_PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)

# setup logging
logfile_path = os.path.join(os.path.abspath("/var/log/inputs"), 'buttons.log')
logfile = open(logfile_path, 'a')  # Open log file in append mode
logging.basicConfig(
    filename=logfile_path,  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


# define variables
def scripts_path():
  """
  Returns the path to the scripts directory.
  """
  return os.path.join(
      os.path.dirname(os.path.abspath(__file__)), "..", "scripts"
  )


# define reset button functions
def on_press():
  """
  Callback function to handle reset button press.
  This function is called when the reset button is pressed.
  """
  logger.info("reset button: calling display_reset and flashing LED")
  press(logger, display_reset, RESET_LED_PIN_OUT, "reset")
  logger.info("reset button pressed, triggering reset action")
  script_path = os.path.join(scripts_path(), "rfids_restart.sh")
  subprocess.Popen(
      ['bash', script_path],
      stdout=logfile,
      stderr=logfile
  )


# avoid spamming by waiting for 2 second before next button press will be registered
# in contrast, the LED will flash when the button is pressed for 1s
logger.info("starting reset button listener...")
try:
  while True:
    listen(
        RESET_BUTTON_PIN_IN,
        on_press=on_press,
        logger=logger,
    )
finally:
  GPIO.cleanup()
