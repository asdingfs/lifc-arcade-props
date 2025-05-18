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
      ['bash', script_path, *args],
      stdout=log_file,
      stderr=log_file
  )
  return push_successful(process, log_file)


def push_successful(
    process: subprocess.Popen,
    log_file
):
  # Check if the process has terminated, and write to log file
  while True:
    exit_code = process.poll()  # None if still running, or exit code if finished
    if exit_code is not None:
      if exit_code != 0:
        log_file.write(f"\nProcess failed with exit code {exit_code}\n")
        log_file.flush()
        log_file.close()
        return False  # only report when it fails
      else:
        log_file.write(
            f"\nProcess completed successfully with exit code {exit_code}\n"
        )
        log_file.flush()
        return True
    else:
      log_file.write("\nProcess is still running...\n")
      log_file.flush()
      time.sleep(1)
