from sqlite3 import Row
from server.utils import uploaded_file_path

class MediaRecord:
  def __init__(self, id: str, url: str, img_src: str):
    self.id = id
    self.url = url
    self.img_src = img_src


  def __repr__(self):
    return f"MediaRecord(id={self.id}, url={self.url})"

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        id=row["id"],
        url=row["url"],
        img_src=uploaded_file_path(row["url"])
    )
