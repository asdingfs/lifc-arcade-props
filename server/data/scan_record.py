from sqlite3 import Row


class ScanRecord:
  def __init__(
      self,
      pkey: int,
      badge_id: int,
      p1_or_p2: bool,
      # TODO: figure out python datatype for sqlite3 Timestamp
      created_at, updated_at,
  ):
    self.pkey = pkey
    self.badge_id = badge_id
    self.p1_or_p2 = p1_or_p2
    self.created_at = created_at
    self.updated_at = updated_at

  def __repr__(self):
    return (
      f"ScanRecord("
      f"id={self.pkey}, badge_id={self.badge_id}, p1_or_p2={self.p1_or_p2}, "
      f"created_at={self.created_at}, updated_at={self.updated_at}"
      f")"
    )

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        pkey=int(row["id"]),
        badge_id=int(row["badge_id"]),
        p1_or_p2=bool(row["p1_or_p2"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )
