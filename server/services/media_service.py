from server.utils import uploaded_file_fullpath
from server.db import get_db
from server.data.media_record import MediaRecord
from werkzeug.utils import secure_filename
from uuid import uuid4


def create_one(media):
  db = get_db()
  cursor = db.cursor()
  filename = secure_filename(str(uuid4()) + '-' + media.filename)
  media.save(uploaded_file_fullpath(filename))
  cursor.execute("INSERT INTO media "
                 "  (url) "
                 "VALUES (?) "
                 "RETURNING *;", (filename,))
  record = cursor.fetchone()
  db.commit()
  return None if record is None else MediaRecord.from_row(record)

def find_one(media):
  db = get_db()
  cursor = db.cursor()
  cursor.execute("SELECT * FROM media WHERE id = ?;", (media,))
  record = cursor.fetchone()
  return None if record is None else MediaRecord.from_row(record)
