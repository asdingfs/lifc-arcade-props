from sqlite3 import Row
from server.utils import uploaded_file_path, arcadeify
from datetime import datetime


class BadgeRecord:
  def __init__(
      self,
      pkey: int,
      code: str,
      name: str,
      media_id: int | None,
      img_src: str | None,
      created_at: datetime | None = None,
      updated_at: datetime | None = None,
  ):
    self.pkey = pkey
    self.code = code
    self.name = name
    self.media_id = media_id
    self.img_src = img_src
    self.created_at = created_at if created_at else datetime.now()
    self.updated_at = updated_at if updated_at else datetime.now()
    self.arcadeify_names()

  def __repr__(self):
    return (f"BadgeRecord("
            f"pkey={self.pkey}, uuid={self.code}, "
            f"name={self.name}, media_id={self.media_id}"
            f")")

  def server_img_src(self):
    return uploaded_file_path(self.img_src)

  def arcadeify_names(self):
    self.name = arcadeify(self.name) if self.name else None

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        pkey=int(row["id"]),
        code=row["code"],
        name=row["name"],
        media_id=int(row["media_id"]) if row["media_id"] else None,
        img_src=row["img_src"] if row["img_src"] else None,
        created_at=row["created_at"] if row["created_at"] else None,
        updated_at=row["updated_at"] if row["updated_at"] else None,
    )

  @classmethod
  def from_request(cls, request):
    media_id = request.form.get("media_id")
    return cls(
        pkey=0,  # pkey is not set during creation, and it's ignored by creation
        code=request.form.get("code"),
        name=request.form.get("name"),
        media_id=int(media_id) if media_id else None,
        img_src=None,  # when creating from request, this is unnecessary
        created_at=None,
        updated_at=None,
    )
