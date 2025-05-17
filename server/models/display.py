from sqlite3 import Row

class Display:
  def __init__(
      self, pkey: int, p1_name: str, p1_img_src: str, p1_score: int,
      p2_name: str, p2_img_src: str, p2_score: int, top_score: int,
      code: str,
  ):
    self.pkey = pkey
    self.p1_name = p1_name
    self.p1_img_src = p1_img_src
    self.p1_score = p1_score
    self.p2_name = p2_name
    self.p2_img_src = p2_img_src
    self.p2_score = p2_score
    self.top_score = top_score
    self.code = code

  def __repr__(self):
    return f"<Display {self.pkey}: {self.p1_name} vs {self.p2_name} (code: {self.code})>"

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        pkey=row["id"],
        p1_name=row["p1_name"],
        p1_img_src=row["p1_img_src"],
        p1_score=row["p1_score"],
        p2_name=row["p2_name"],
        p2_img_src=row["p2_img_src"],
        p2_score=row["p2_score"],
        top_score=row["top_score"],
        code=row["code"]
    )