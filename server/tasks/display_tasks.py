from server.data.display_state import DisplayState
from server.services import scheduler_service

scheduler = scheduler_service.get_scheduler()
app = scheduler.app

# interval example
@scheduler.task(
    'interval',
    id='periodic_display_reset',
    seconds=5,
    misfire_grace_time=900
)
def display_reset():
  print('Executing periodic display reset...')
  with app.app_context():
    display = DisplayState()
    display.regress()
    display.sync()
  print('Display reset executed successfully!')
