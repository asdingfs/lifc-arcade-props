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

# Set the desired interface to True
SPI = False

if SPI:
  PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
  nfc = Pn532(PN532_SPI)


def setup():
  nfc.begin()

  firmware = nfc.getFirmwareVersion()
  if not firmware:
    print("Didn't find PN53x board")
    raise RuntimeError("Didn't find PN53x board")  # halt

  # Got ok data, print it out!
  print(
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

  print("Waiting for an ISO14443A card...")


def loop():
  # Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
  # 'uid' will be populated with the UID, and uidLength will indicate
  # if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
  success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

  if success:
    print("Found a card!")
    print("UID Length: {:d}".format(len(uid)))
    print("UID Value: {}".format(binascii.hexlify(uid)))
    # Wait 1 second before continuing
    time.sleep(1)
    return True
  else:
    # pn532 probably timed out waiting for a card
    print("Timed out waiting for a card!")
    return False


if __name__ == '__main__':
  setup()
  found = loop()
  while not found:
    found = loop()
