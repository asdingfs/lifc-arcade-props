import RPi.GPIO as GPIO
from concurrent.futures import ThreadPoolExecutor
import time


def led_on(pin):
  """Turns the LED on."""
  GPIO.output(pin, GPIO.LOW)


def led_off(pin):
  """Turns the LED off."""
  GPIO.output(pin, GPIO.HIGH)


def press(logger, api, led_pin):
  """Handle the button press event."""
  # This function can be customized to perform any action when the button is pressed.
  logger.info("reset button pressed!")
  with ThreadPoolExecutor() as executor:
    led_future = executor.submit(flash_led, led_pin, 1, 1)
    request_future = executor.submit(api, logger)
    try:
      if request_future.result(timeout=4):
        return  # if successful, start button script loop is done
      else:
        led_future.result(timeout=4)
        flash_led(led_pin, 3, 0.25)
    except TimeoutError:
      logger.error("one of the task timed out, flash error")
      flash_led(led_pin, 3, 0.25)
      led_future.cancel()
      request_future.cancel()


def flash_led(pin, times, duration=0.5):
  """Flashes the LED a specified number of times."""
  for _ in range(times):
    led_on(pin)
    time.sleep(duration)
    led_off(pin)
    time.sleep(duration)


def listen(pin, on_press, logger=None):
  if GPIO.input(pin) == GPIO.HIGH:
    try:
      on_press()
    except Exception as ex:
      logger and logger.error(
          f"Exception during button press action: "
          f"{ex}, {type(ex).__name__}"
      )
