from server.db import get_db
from server.data.scan_record import ScanRecord


def find_one(pkey: int):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      """
              SELECT s.* FROM scan s
              WHERE s.id = ?;
        """, (pkey,)
  )
  record = cursor.fetchone()
  return None if record is None else ScanRecord.from_row(record)


# p1_or_p2: boolean. True -> P1, False -> P2
def create_one(badge_id: int, p1_or_p2: bool):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      "INSERT INTO scan "
      "  (badge_id, p1_or_p2) "
      "VALUES (?, ?) "
      "RETURNING *;", (badge_id, p1_or_p2,)
  )
  record = cursor.fetchone()
  db.commit()
  return None if record is None else ScanRecord.from_row(record)


def find_latest_p1():
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      "SELECT * FROM scan WHERE p1_or_p2 = TRUE ORDER BY updated_at DESC LIMIT 1;"
  )
  record = cursor.fetchone()
  return None if record is None else ScanRecord.from_row(record)


def find_latest_p2():
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      "SELECT * FROM scan WHERE p1_or_p2 = FALSE ORDER BY updated_at DESC LIMIT 1;"
  )
  record = cursor.fetchone()
  return None if record is None else ScanRecord.from_row(record)
