from flask import current_app, url_for
from server.data.display_view import DisplayView
import os
import subprocess
import time

app = current_app


def scripts_path():
  return os.path.abspath(os.path.join(app.root_path, "..", "scripts"))

def previews_path():
  return os.path.abspath(os.path.join(app.root_path, "static"))


def push(display: DisplayView):
  script_path = os.path.join(scripts_path(), "async_single_renderer.sh")
  log_path = os.path.join(scripts_path(), "processing-java.log")
  log_file = open(log_path, "a")
  args = display.to_cli_args()
  # run processing-java in background
  process = subprocess.Popen(
      ['bash', script_path, *args],
      stdout=log_file,
      stderr=log_file
  )
  return poll_exec(process, log_file)


def preview(display: DisplayView):
  script_path = os.path.join(scripts_path(), "sync_multiple_renderer.sh")
  filename = f"previews/{display.code}.png"
  os_img_path = os.path.join(previews_path(), filename)
  ws_img_path = url_for('static', filename=filename)
  log_path = os.path.join(scripts_path(), "processing-java.log")
  log_file = open(log_path, "a")
  args = display.to_cli_args()
  args.append(f"--savePreview={os_img_path}")
  # run processing-java in background
  process = subprocess.Popen(
      ['bash', script_path, *args],
      stdout=log_file,
      stderr=log_file
  )
  is_successful = poll_exec(process, log_file)
  if is_successful:
    log_file.write(f"\nPreview successfully saved to {os_img_path}\n")
  else:
    log_file.write(f"\nGenerating preview FAILED!\n")
  log_file.flush()
  log_file.close()
  return ws_img_path if is_successful else None


def poll_exec(process: subprocess.Popen, log_file):
  # Check if the process has terminated, and write to log file
  while True:
    exit_code = process.poll()  # None if still running, or exit code if finished
    if exit_code is not None:
      if exit_code != 0:
        log_file.write(f"\nProcess failed with exit code {exit_code}\n")
        log_file.flush()
        log_file.close()
        return False
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
