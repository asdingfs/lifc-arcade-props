# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from server import create_app
from server.data.display_state import DisplayState

application = create_app()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  with application.app_context():
    DisplayState().sync()  # Ensure the display state is synced on startup
  application.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
