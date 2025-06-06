from server.db import get_db, close_db
from server.data.display_view import DisplayView

# NOTE: this records, always return one more... for infinite scrolling
def find_all(search: str | None = None, page: int = 0, size: int = 20):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      f'''
      SELECT d.*,
             m1.url as p1_img_src,
             m2.url as p2_img_src
      FROM display d
               LEFT JOIN media m1 ON d.p1_media_id = m1.id
               LEFT JOIN media m2 ON d.p2_media_id = m2.id
      {"WHERE (d.p1_name LIKE ? OR d.p2_name LIKE ?)" if search else ""}
      ORDER BY d.updated_at DESC
      LIMIT ? OFFSET ?;
      ''',
      (*((f"%{search}%", f"%{search}%") if search else ()),
       *(size + 1, page * size)),

  )
  records = cursor.fetchall()
  close_db()  # Close the DB connection after query
  top = top_score()
  return [DisplayView.from_row(row, top) for row in records]


def find_one(pkey):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      SELECT d.*,
             m1.url as p1_img_src,
             m2.url as p2_img_src
      FROM display d
               LEFT JOIN media m1 ON d.p1_media_id = m1.id
               LEFT JOIN media m2 ON d.p2_media_id = m2.id
      WHERE d.id = ?;
      ''', (pkey,)
  )
  record = cursor.fetchone()
  close_db()
  return None if record is None else DisplayView.from_row(record, top_score())


def create_one(display):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      INSERT INTO display (p1_name, p1_media_id, p1_score,
                           p2_name, p2_media_id, p2_score,
                           code)
      VALUES (?, ?, ?, ?, ?, ?, ?);
      ''',
      (
        display.p1_name,
        display.p1_media_id,
        display.p1_score,
        display.p2_name,
        display.p2_media_id,
        display.p2_score,
        display.code,
      )
  )
  created_id = cursor.lastrowid
  db.commit()
  close_db()  # Close the DB connection after query
  return None if created_id is None else find_one(created_id)


def update_one(pkey, display):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      UPDATE display
      SET p1_name     = ?,
          p1_media_id = ?,
          p1_score    = ?,
          p2_name     = ?,
          p2_media_id = ?,
          p2_score    = ?,
          code        = ?
      WHERE id = ?;
      ''',
      (
        display.p1_name,
        display.p1_media_id,
        display.p1_score,
        display.p2_name,
        display.p2_media_id,
        display.p2_score,
        display.code,
        pkey,
      )
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
      FROM display
      WHERE id = ?;
      ''',
      (pkey,)
  )
  db.commit()
  close_db()  # Close the DB connection after query
  return None


def top_score():
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      SELECT MAX(MAX(p1_score), MAX(p2_score)) as top_score
      FROM display;
      '''
  )
  record = cursor.fetchone()
  close_db()  # Close the DB connection after query
  return None if record is None else record["top_score"]


def reset_scores():
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
      UPDATE display
      SET p1_score = 0,
          p2_score = 0;
      '''
  )
  db.commit()
  close_db()  # Close the DB connection after query
  return None
