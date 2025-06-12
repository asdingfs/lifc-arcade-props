#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python
"""
    based on example from: pn532pi library
    To enable debug message, set DEBUG in nfc/PN532_log.h
"""
import logging
import os
import time
import asyncio
import threading
import RPi.GPIO as GPIO
from pn532pi import Pn532, pn532, Pn532Spi
from rfid_reader import setup, read, log
from constants import PLAYER_1_RFID_SS_PIN, BUZZER_RIGHT_PIN_OUT
from apis import register_p1

# setup buzzer GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZZER_RIGHT_PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)

# and lock, so that the buzzer sounds will not overlap
lock = threading.Lock()

# setup logging
logging.basicConfig(
    filename=os.path.join(os.path.abspath("/var/log/inputs"), 'readers.log'),
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)

# setup player 1 RFID reader SPI
PN532_SPI = Pn532Spi(PLAYER_1_RFID_SS_PIN)
nfc = Pn532(PN532_SPI)
if setup(nfc, PLAYER_1_RFID_SS_PIN, logger):
  log(logger.info, PLAYER_1_RFID_SS_PIN, "setup successfully!")
else:
  log(logger.error, PLAYER_1_RFID_SS_PIN, "setup failed!")
  raise RuntimeError("Failed to setup player 1 RFID reader.")


async def buzz(pin, up=0.2, down=0.2, times=1):
  """
  Buzzes the buzzer connected to the specified pin.
  """
  with lock:
    for _ in range(times):
      GPIO.output(pin, GPIO.LOW)
      time.sleep(up)
      GPIO.output(pin, GPIO.HIGH)
      time.sleep(down)


def on_detect(_):
  """
  Callback function to handle detection of a card.
  This function is called when a card is detected.
  """
  asyncio.run(buzz(BUZZER_RIGHT_PIN_OUT, up=0.1, down=0.1, times=1))
  return True


# define on_read function
def on_read(uid):
  if register_p1(uid, logger):
    asyncio.run(buzz(BUZZER_RIGHT_PIN_OUT, up=0.1, down=0.05, times=2))
    return True
  else:
    asyncio.run(buzz(BUZZER_RIGHT_PIN_OUT, up=1, down=0.1, times=1))
    return False


try:
  while True:
    read(
        nfc, PLAYER_1_RFID_SS_PIN, logger,
        on_detect=on_detect,
        on_read=on_read
    )
finally:
  GPIO.cleanup()
