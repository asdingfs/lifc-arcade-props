from server.utils import allowed_file, uploaded_file_fullpath
from server.db import get_db
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from uuid import uuid4


def create_players_media(p1_media: FileStorage, p2_media: FileStorage):
  db = get_db()
  cursor = db.cursor()
  # create for p1
  p1_filename = secure_filename(str(uuid4()) + p1_media.filename)
  p1_media.save(uploaded_file_fullpath(p1_filename))
  cursor.execute("INSERT INTO media (url) VALUES (?)", (p1_filename,))
  p1_created_id = cursor.lastrowid
  # create for p2
  p2_filename = secure_filename(str(uuid4()) + p2_media.filename)
  p2_media.save(uploaded_file_fullpath(p2_filename))
  cursor.execute("INSERT INTO media (url) VALUES (?)", (p2_filename,))
  p2_created_id = cursor.lastrowid
  # commit, and return
  db.commit()

  return p1_created_id, p2_created_id
