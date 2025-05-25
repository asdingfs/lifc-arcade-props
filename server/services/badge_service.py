from server.db import get_db
from server.data.badge_record import BadgeRecord
import random

DEFAULT_CODES = [
  "default_1",
  "default_2",
  "default_3",
]


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
  return None if record is None else BadgeRecord.from_row(record)


def find_one_random_default():
  return find_one_by_uuid(random.choice(DEFAULT_CODES))
