import sqlite3
import threading
from queue import Queue, Empty


class DbConnectionPool:
  def __init__(self, db_path, max_size=5):
    self._db_path = db_path
    self._pool = Queue(maxsize=max_size)
    self._lock = threading.Lock()

    # Pre-populate the pool
    for _ in range(max_size):
      db_conn = sqlite3.connect(
          self._db_path,
          detect_types=sqlite3.PARSE_DECLTYPES,
      )
      db_conn.row_factory = sqlite3.Row
      self._pool.put(db_conn)

  def get(self, timeout=4):
    try:
      with self._lock:
        return self._pool.get(timeout=timeout)
    except Empty:
      raise Exception("No available connections in the pool.")

  def forgo(self, db_conn):
    if db_conn:
      with self._lock:
        self._pool.put(db_conn)

  def close_all(self):
    while not self._pool.empty():
      db_conn = self._pool.get_nowait()
      db_conn.close()
