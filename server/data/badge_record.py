from sqlite3 import Row


class BadgeRecord:
  def __init__(
      self,
      pkey: int,
      code: str,
      name: str,
      media_id: int | None,
      img_src: str | None,
  ):
    self.pkey = pkey
    self.code = code
    self.name = name
    self.media_id = media_id
    self.img_src = img_src

  def __repr__(self):
    return (f"BadgeRecord("
            f"id={self.pkey}, uuid={self.code}, "
            f"name={self.name}, media_id={self.media_id}"
            f")")

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        pkey=int(row["id"]),
        code=row["code"],
        name=row["name"],
        media_id=int(row["media_id"]) if row["media_id"] else None,
        img_src=row["img_src"] if "img_src" in row else None
    )
