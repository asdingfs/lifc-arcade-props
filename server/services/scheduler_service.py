import threading
from flask_apscheduler import APScheduler


def get_scheduler():
  return SchedulerService()


class SchedulerService:
  _instance = APScheduler()
  _lock = threading.Lock()

  def __new__(cls):
    if cls._instance is None:
      with cls._lock:
        # Another thread could have created the instance
        # before we acquired the lock. So check that the
        # instance is still non-existent.
        if not cls._instance:
          cls._instance = super().__new__(cls)
    return cls._instance
