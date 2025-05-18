from sqlite3 import Row
from server.utils import uploaded_file_path


class DisplayView:
  def __init__(
      self, pkey: int, code: str,
      p1_name: str, p1_img_src: str, p1_media_id: int, p1_score: int,
      p2_name: str, p2_img_src: str, p2_media_id: int, p2_score: int,
      top_score: int,
  ):
    self.pkey = pkey
    self.code = code
    self.p1_name = p1_name
    self.p1_img_src = p1_img_src
    self.p1_media_id = p1_media_id
    self.p1_score = p1_score
    self.p2_name = p2_name
    self.p2_img_src = p2_img_src
    self.p2_media_id = p2_media_id
    self.p2_score = p2_score
    self.top_score = top_score

  def __repr__(self):
    return (f"<Display {self.pkey} (code: {self.code}): "
            f"{self.p1_name} (score: {self.p1_score}, "
            f"img_src: {self.p1_img_src}, media_id: {self.p1_media_id}) vs "
            f"{self.p2_name} (score: {self.p2_score}"
            f"img_src: {self.p2_img_src}, media_id: {self.p2_media_id})"
            f", top score: {self.top_score} "
            f">")

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        pkey=row["id"],
        code=row["code"],
        p1_name=row["p1_name"],
        p1_img_src=uploaded_file_path(row["p1_img_src"]),
        p1_media_id = row["p1_media_id"],
        p1_score=row["p1_score"],
        p2_name=row["p2_name"],
        p2_img_src=uploaded_file_path(row["p2_img_src"]),
        p2_media_id = row["p2_media_id"],
        p2_score=row["p2_score"],
        top_score=row["top_score"],
    )
