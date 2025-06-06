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


def logfile_path():
  return os.path.join(scripts_path(), "processing-java.log")


def push(display: DisplayView):
  script_path = os.path.join(scripts_path(), "bg_draw_update.sh")
  logfile = open(logfile_path(), "a")
  args = display.to_cli_args()
  # run processing-java in background
  process = subprocess.Popen(
      ['bash', script_path, *args],
      stdout=logfile,
      stderr=logfile
  )
  return poll_exec(process, logfile)


def preview(display: DisplayView):
  script_path = os.path.join(scripts_path(), "fg_draw_create.sh")
  filename = f"previews/{display.code}.png"
  os_img_path = os.path.join(previews_path(), filename)
  ws_img_path = url_for('static', filename=filename)
  logfile = open(logfile_path(), "a")
  args = display.to_cli_args()
  args.append(f"--savePreview={os_img_path}")
  # run processing-java in background
  process = subprocess.Popen(
      ['bash', script_path, *args],
      stdout=logfile,
      stderr=logfile
  )
  is_successful = poll_exec(process, logfile)
  if is_successful:
    logfile.write(f"\nPreview successfully saved to {os_img_path}\n")
  else:
    logfile.write(f"\nGenerating preview FAILED!\n")
  logfile.flush()
  logfile.close()
  return (os_img_path, ws_img_path) if is_successful else (None, None)


def download(display: DisplayView):
  os_path, _ = preview(display)
  if os_path:
    filename = os.path.basename(os_path)
    mimetype = "image/png"
    return os_path, filename, mimetype
  else:
    # If preview generation failed, return None values
    app.logger.error(f"failed to generate preview for display {display.code}")
    return None, None, None


def poll_exec(process: subprocess.Popen, logfile):
  # Check if the process has terminated, and write to log file
  while True:
    exit_code = process.poll()  # None if still running, or exit code if finished
    if exit_code is not None:
      if exit_code != 0:
        logfile.write(f"\nProcess failed with exit code {exit_code}\n")
        logfile.flush()
        logfile.close()
        return False
      else:
        logfile.write(
            f"\nProcess completed successfully with exit code {exit_code}\n"
        )
        logfile.flush()
        return True
    else:
      logfile.write("\nProcess is still running...\n")
      logfile.flush()
      time.sleep(1)
