from server.db import get_db, close_db
from server.data.badge_record import BadgeRecord
import random

DEFAULT_CODES = [
  "default_1",
  "default_2",
  "default_3",
]


def find_by_codes(codes: list[str]):
  if not codes:
    return []
  db = get_db()
  cursor = db.cursor()
  placeholders = ', '.join(['?'] * len(codes))
  cursor.execute(
      f'''
        SELECT b.*,
          m.url as img_src
        FROM badge b
        LEFT JOIN media m ON b.media_id = m.id
        WHERE b.code IN ({placeholders});
      ''', tuple(codes)
  )
  records = cursor.fetchall()
  close_db()  # Close the DB connection after query
  return [BadgeRecord.from_row(record) for record in records]


def find_one(pkey):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      SELECT b.*
      FROM badge b
      WHERE b.id = ?;
      ''', (pkey,)
  )
  record = cursor.fetchone()
  close_db()  # Close the DB connection after query

  return None \
    if record is None \
    else BadgeRecord.from_row(record)  # NOTE: no img_src


def find_one_by_uuid(uuid):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      SELECT b.*,
             m.url as img_src
      FROM badge b
               LEFT JOIN media m ON b.media_id = m.id
      WHERE b.code = ?;
      ''', (uuid,)
  )
  record = cursor.fetchone()
  close_db()  # Close the DB connection after query
  return None if record is None else BadgeRecord.from_row(record)


def find_random_defaults(n: int = 1):
  if n < 1 or n > len(DEFAULT_CODES):
    raise ValueError(f"n must be between 1 and {len(DEFAULT_CODES)}")
  return find_by_codes(random.sample(DEFAULT_CODES, n))
