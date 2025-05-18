from server.utils import uploaded_file_fullpath
from server.db import get_db
from werkzeug.utils import secure_filename
from uuid import uuid4


def create_one(media):
  db = get_db()
  cursor = db.cursor()
  filename = secure_filename(str(uuid4()) + media.filename)
  media.save(uploaded_file_fullpath(filename))
  cursor.execute("INSERT INTO media (url) VALUES (?)", (filename,))
  created_id = cursor.lastrowid
  db.commit()
  return created_id
