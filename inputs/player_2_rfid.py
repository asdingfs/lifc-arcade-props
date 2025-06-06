#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python
"""
    based on example from: pn532pi library
    To enable debug message, set DEBUG in nfc/PN532_log.h
"""
import logging
import os
from pn532pi import Pn532, pn532, Pn532Spi
from rfid_reader import setup, read, log
from constants import PLAYER_2_RFID_SS_PIN
from apis import register_p2

# setup logging
logging.basicConfig(
    filename=os.path.join(os.path.abspath("/var/log/inputs"), 'readers.log'),
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)

# setup player 1 RFID reader SPI
PN532_SPI = Pn532Spi(PLAYER_2_RFID_SS_PIN)
nfc = Pn532(PN532_SPI)
if setup(nfc, PLAYER_2_RFID_SS_PIN, logger):
  log(logger.info, PLAYER_2_RFID_SS_PIN, "setup successfully!")
else:
  log(logger.error, PLAYER_2_RFID_SS_PIN, "setup failed!")

while True:
  read(
      nfc, PLAYER_2_RFID_SS_PIN, logger,
      on_read=lambda uid: register_p2(uid, logger),
  )
