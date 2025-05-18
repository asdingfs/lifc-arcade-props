from flask import current_app
from server.data.display_view import DisplayView
import os
import subprocess
import time

app = current_app


def scripts_path():
  return os.path.abspath(os.path.join(app.root_path, "..", "scripts"))


def push(display: DisplayView):
  script_path = os.path.join(scripts_path(), "send_to_local.sh")
  log_path = os.path.join(scripts_path(), "processing-java.log")
  log_file = open(log_path, "a")
  args = display.to_cli_args()
  # run processing-java in background
  process = subprocess.Popen(
      [script_path, *args],
      stdout=log_file,
      stderr=log_file
  )
  return is_running(process, log_file)


def is_running(
    process: subprocess.Popen,
    log_file
):
  wait_time = 2
  time.sleep(wait_time)  # Wait for #wait_time seconds

  # Check if the process has terminated, and write to log file
  exit_code = process.poll()  # None if still running, or exit code if finished
  if exit_code is not None:
    if exit_code != 0:
      log_file.write(f"\nProcess failed with exit code {exit_code}\n")
      log_file.flush()
      log_file.close()
    else:
      log_file.write(
          f"\nProcess completed successfully with exit code {exit_code}\n"
      )
      log_file.flush()
    return False  # Not running
  else:
    log_file.write("\nProcess is still running after 3 seconds.\n")
    log_file.flush()
    # Do not close log_file yet, process may still write to it
    return True  # Still running
