#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python
"""
    This example will attempt to connect to an ISO14443A
    card or tag and retrieve some basic information about it
    that can be used to determine what type of card it is.

    will attempt to read two readers at once

    To enable debug message, set DEBUG in nfc/PN532_log.h
"""

import logging
import os
from constants import PLAYER_1_RFID_SS_PIN, PLAYER_2_RFID_SS_PIN
from pn532pi import Pn532, pn532, Pn532Spi
from rfid_reader import setup, read, log

# setup logging
script_dir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
  filename=os.path.join(script_dir, 'readers.log'),
  level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# setup player 1 RFID reader on SPI
p1_reader = Pn532(Pn532Spi(PLAYER_1_RFID_SS_PIN))
if setup(p1_reader, PLAYER_1_RFID_SS_PIN, logger):
  log(logger.info, PLAYER_1_RFID_SS_PIN, "setup successfully!")
else:
  log(logger.error, PLAYER_1_RFID_SS_PIN, "setup failed!")

# setup player 2 RFID reader on SPI
# p2_reader = Pn532(Pn532Spi(PLAYER_2_RFID_SS_PIN))
# if setup(p2_reader, PLAYER_2_RFID_SS_PIN, logger):
#   log(logger.info, PLAYER_2_RFID_SS_PIN, "setup successfully!")
# else:
#   log(logger.error, PLAYER_2_RFID_SS_PIN, "setup failed!")

# start listening for RFID tags on both readers
while True:
  p1_uid = read(p1_reader, PLAYER_1_RFID_SS_PIN, logger)
  # p2_uid = read(p2_reader, PLAYER_2_RFID_SS_PIN, logger)
