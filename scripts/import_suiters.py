import pandas as pd
import anyascii
import sys
import sqlite3
import os
import shutil
from werkzeug.utils import secure_filename
from sqlite3 import Cursor, Row
from typing import BinaryIO
from uuid import uuid4

# setup migration constants
SERVER_APP_ROOT = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '..',
)
UPLOAD_FOLDER = os.path.join(SERVER_APP_ROOT, 'server', 'static', 'uploads')
BADGE_NUMBER_COLUMN = 'Badge Number'
BADGE_NAME_COLUMN = 'Fursuit Name'
AVATAR_URL_COLUMN = 'Avatar'
BADGE_RFID_UID_COLUMN = 'UID'

# setting path
sys.path.append(f'{SERVER_APP_ROOT}/server/data')
sys.path.append(f'{SERVER_APP_ROOT}/server/services')


def find_unique_file_with_prefix(directory, prefix) -> list[str]:
  """
  Find a unique file in the given directory with the specified prefix.
  """
  files = [os.path.join(directory, f) for f in
           os.listdir(os.path.abspath(directory)) if
           f.lower().startswith(prefix.lower())]
  if len(files) > 1:
    print(f"Multiple files ({len(files)}) found with prefix '{prefix}'")
  return files


def format_number(number: int) -> str:
  return str(number).rjust(3, "0")


def get_db():
  return sqlite3.connect(
      os.path.join(SERVER_APP_ROOT, 'instance', 'server.sqlite'),
      detect_types=sqlite3.PARSE_DECLTYPES,
  )


def close_db(db):
  if db is not None:
    db.close()


def create_one_media(cursor: Cursor, file: BinaryIO, ) -> int | None:
  filename = secure_filename(str(uuid4()) + '-' + os.path.basename(file.name))
  source = os.path.abspath(file.name)
  destination = os.path.join(UPLOAD_FOLDER, filename)
  shutil.copy2(source, destination)
  cursor.execute(
      "INSERT INTO media "
      "  (url) "
      "VALUES (?) "
      "RETURNING *;", (filename,)
  )
  record = cursor.fetchone()
  conn.commit()
  return int(record["id"]) if record else None


def create_one_badge(
    cursor: Cursor,
    code: str, name: str, media_id: int | None
) -> int | None:
  cursor.execute(
      '''
      INSERT INTO badge (code, name, media_id)
      VALUES (?, ?, ?);
      ''',
      (
        code.upper(),
        name,
        media_id,
      )
  )
  record = cursor.fetchone()
  conn.commit()
  return int(record["id"]) if record else None


df = pd.read_excel(
    os.path.join(SERVER_APP_ROOT, 'instance', 'fursuiter.xlsx'),
    dtype={
      BADGE_NUMBER_COLUMN: int, BADGE_NAME_COLUMN: str,
      AVATAR_URL_COLUMN: str, BADGE_RFID_UID_COLUMN: str
    }
)

conn = get_db()
conn.row_factory = Row
cur = conn.cursor()
count_no_avatars = 0
count_missing_avatars = 0
count_valid_avatars = 0
count_all_avatars = 0
multiple_number_count = 1

for i, row in df.iterrows():
  badge_number = row[BADGE_NUMBER_COLUMN]
  badge_actual_name = row[BADGE_NAME_COLUMN]
  badge_name = anyascii.anyascii(row[BADGE_NAME_COLUMN]).upper()
  badge_rfid_uid = row[BADGE_RFID_UID_COLUMN].upper()
  badge_avatar_url = row[AVATAR_URL_COLUMN]
  badge_avatar_url = '' if pd.isna(
      badge_avatar_url
  ) else badge_avatar_url.strip()
  filepaths = find_unique_file_with_prefix(
      "../instance/images/fursuits/",
      f"{format_number(badge_number)} - {badge_actual_name}"
  )

  # upload avatar is available, otherwise set media to None
  media_id = None
  count_all_avatars += 1
  if len(filepaths) == 0:
    if badge_avatar_url:
      print(
          f"WARNING: [B#{format_number(badge_number)}] "
          f"No file found for badge number even though URL in Excel exists!"
      )
      print()
      count_missing_avatars += 1
    else:
      print(
          f"[B#{format_number(badge_number)}] "
          f"{badge_name} has no avatar"
      )
      count_no_avatars += 1
    multiple_number_count = 1
  elif len(filepaths) == 1:
    print(
        f"[B#{format_number(badge_number)}] "
        f"{badge_name} has avatar at {filepaths[0]}"
    )
    media_id = create_one_media(cur, open(filepaths[0], 'rb'))
    count_valid_avatars += 1
    multiple_number_count = 1
  else:
    print(
        f"[B#{format_number(badge_number)}] "
        f"{badge_name} has multiple avatars at {filepaths}"
    )
    duplicate_filepaths = find_unique_file_with_prefix(
        "../instance/images/fursuits/",
        f"{format_number(badge_number)} - {badge_actual_name} "
        f"({multiple_number_count})"
    )

    if len(duplicate_filepaths) == 0:
      if badge_avatar_url:
        print(
            f"WARNING: [B#{format_number(badge_number)} ({multiple_number_count})] "
            f"No file found for badge number even though URL in Excel exists!"
        )
        count_missing_avatars += 1
      else:
        print(
            f"[B#{format_number(badge_number)} ({multiple_number_count})] "
            f"{badge_name} has no avatar"
        )
        count_no_avatars += 1
    elif len(duplicate_filepaths) == 1:
      print(
          f"[B#{format_number(badge_number)} ({multiple_number_count})] "
          f"{badge_name} has avatar at {duplicate_filepaths[0]}"
      )
      count_valid_avatars += 1
      media_id = create_one_media(cur, open(filepaths[0], 'rb'))
    else:
      raise ValueError(
          f"Multiple files ({len(filepaths)}) found with prefix "
          f"'{format_number(badge_number)} - {badge_actual_name} "
          f"({multiple_number_count})'"
      )

    multiple_number_count += 1
  # create badge record
  create_one_badge(cur, badge_rfid_uid, badge_name, media_id)

close_db(conn)
print(
    f"total avatars: {count_all_avatars} "
    f"(valid + missing + none: "
    f"{count_valid_avatars} + "
    f"{count_missing_avatars} + "
    f"{count_no_avatars})"
)
