#!/home/trigger/lifc-arcade-props/inputs/.venv/bin/python
"""
    This example will attempt to connect to an ISO14443A
    card or tag and retrieve some basic information about it
    that can be used to determine what type of card it is.

    To enable debug message, set DEBUG in nfc/PN532_log.h
"""
import time
import binascii
from pn532pi import Pn532, pn532, Pn532Spi


def log(logger_level, ss_pin, message):
  logger_level(f"[Reader-SS#{ss_pin}]: {message}")


def setup(nfc, ss_pin, logger, retry=3):
  nfc.begin()

  # print out firmware version
  firmware = nfc.getFirmwareVersion()
  if not firmware:
    if retry > 0:
      log(logger.warning, ss_pin, "Couldn't find PN53x board, retrying...")
      time.sleep(1)
      return setup(nfc, ss_pin, logger, retry - 1)
    else:
      # If we reach here, it means we have exhausted all retries
      # and still couldn't find the PN53x board.
      # Log an error message and return False.
      log(logger.error, ss_pin, "Couldn't find PN53x board even after retries!")
      return False
  else:
    # print firmware version
    log(
        logger.info, ss_pin,
        "Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format(
            (firmware >> 24) & 0xFF, (firmware >> 16) & 0xFF,
            (firmware >> 8) & 0xFF
        )
    )
    # Set the max number of retry attempts to read from a card
    # This prevents us from waiting forever for a card, which is
    # the default behaviour of the pn532.
    nfc.setPassiveActivationRetries(0xFF)

    # configure board to read RFID tags
    nfc.SAMConfig()
    log(
        logger.info, ss_pin,
        "Successfully setup! Waiting for an ISO14443A card..."
    )
    return True  # indicates setup was successful


def read(nfc, ss_pin, logger):
  # Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
  # 'uid' will be populated with the UID, and uidLength will indicate
  # if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
  success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
  if success:
    log(logger.info, ss_pin, "Found a tag!")
    log(logger.info, ss_pin, "UID Length: {:d}".format(len(uid)))
    log(logger.info, ss_pin, "UID Value: {}".format(binascii.hexlify(uid)))
    time.sleep(1)
    return binascii.hexlify(uid).decode('utf-8')  # return UID as a string
  else:
    # pn532 probably timed out waiting for a card
    log(logger.debug, ss_pin, "Timed out waiting for a card!")
    return None
