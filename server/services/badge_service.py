from server.db import get_db, close_db
from server.data.badge_record import BadgeRecord
import random

DEFAULT_CODES = [
  "default_1",
  "default_2",
  "default_3",
]


def find_all(search: str | None = None, page: int = 0, size: int = 20):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      f'''
      SELECT b.*,
             m.url as img_src
      FROM badge b
               LEFT JOIN media m ON b.media_id = m.id
      {"WHERE (b.code LIKE ? OR b.name LIKE ?)" if search else ""}
      ORDER BY b.updated_at DESC
      LIMIT ? OFFSET ?;
      ''',
      (*((f"%{search}%", f"%{search}%") if search else ()),
       *(size + 1, page * size)),
  )
  records = cursor.fetchall()
  close_db()  # Close the DB connection after query
  return [BadgeRecord.from_row(record) for record in records]


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
      SELECT b.*,
             m.url as img_src
      FROM badge b
               LEFT JOIN media m ON b.media_id = m.id
      WHERE b.id = ?;
      ''', (pkey,)
  )
  record = cursor.fetchone()
  close_db()  # Close the DB connection after query
  # NOTE: no img_src
  return None if record is None else BadgeRecord.from_row(record)


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
  defaults = random.sample(DEFAULT_CODES, n)
  random.shuffle(defaults)  # Shuffle to ensure randomness
  return find_by_codes(defaults)


def create_one(badge):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      INSERT INTO badge (code, name, media_id)
      VALUES (?, ?, ?);
      ''',
      (
        badge.code,
        badge.name,
        badge.media_id,
      )
  )
  created_id = cursor.lastrowid
  db.commit()
  close_db()  # Close the DB connection after query
  return None if created_id is None else find_one(created_id)


def update_one(pkey, badge: BadgeRecord):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      UPDATE badge
      SET code     = ?,
          name     = ?,
          media_id = ?
      WHERE id = ?;
      ''',
      (badge.code, badge.name, badge.media_id, pkey,)
  )
  db.commit()
  close_db()  # Close the DB connection after query
  return find_one(pkey)

def delete_one(pkey):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      DELETE
      FROM badge
      WHERE id = ?;
      ''',
      (pkey,)
  )
  db.commit()
  close_db()  # Close the DB connection after query
  return None
