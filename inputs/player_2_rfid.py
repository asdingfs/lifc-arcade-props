#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python
"""
    based on example from: pn532pi library
    To enable debug message, set DEBUG in nfc/PN532_log.h
"""
import logging
import time
import os
from pn532pi import Pn532, pn532, Pn532Spi
from rfid_reader import setup, read, log
from constants import PLAYER_2_RFID_SS_PIN

# setup logging
script_dir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(script_dir, 'readers.log'),
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)

# setup player 1 RFID reader SPI
PN532_SPI = Pn532Spi(PLAYER_2_RFID_SS_PIN)
nfc = Pn532(PN532_SPI)
setup(nfc, PLAYER_2_RFID_SS_PIN, logger)

while True:
  uid = read(nfc, PLAYER_2_RFID_SS_PIN, logger)
  if uid:
    # TODO: process the UID
    pass
  else:
    log(logger.error, PLAYER_2_RFID_SS_PIN, "No card detected or read failed.")
  time.sleep(2)  # wait before next read attempt
