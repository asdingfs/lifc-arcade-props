from server.db import get_db
from server.data.display_view import DisplayView


def find_all():
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
          SELECT d.*,
            m1.url as p1_img_src,
            m2.url as p2_img_src,
            MAX(d.p1_score, d.p2_score) as top_score
          FROM display d
          LEFT JOIN media m1 ON d.p1_media_id = m1.id
          LEFT JOIN media m2 ON d.p2_media_id = m2.id
          ORDER BY d.created_at DESC
      '''
  )
  entries = cursor.fetchall()

  return [DisplayView.from_row(row) for row in entries]


def find_one(pkey):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
        SELECT d.*,
          m1.url as p1_img_src,
          m2.url as p2_img_src,
          MAX(d.p1_score, d.p2_score) as top_score
        FROM display d
        LEFT JOIN media m1 ON d.p1_media_id = m1.id
        LEFT JOIN media m2 ON d.p2_media_id = m2.id
        WHERE d.id = ?
      ''', (pkey,)
  )
  entry = cursor.fetchone()

  return None if entry is None else DisplayView.from_row(entry)


def create_one(display):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
        INSERT INTO display (
          p1_name, p1_media_id, p1_score,
          p2_name, p2_media_id, p2_score,
          code, feedback
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      ''',
      (
        display.p1_name,
        display.p1_media_id,
        display.p1_score,
        display.p2_name,
        display.p2_media_id,
        display.p2_score,
        display.code,
        display.feedback
      )
  )
  created_id = cursor.lastrowid
  db.commit()

  return created_id
