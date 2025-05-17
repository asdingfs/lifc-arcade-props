from flask import Request
from sqlite3 import Row
from uuid import uuid4


class DisplayRow:
  def __init__(
      self,
      p1_name: str, p1_media_id: int | None, p1_score: int,
      p2_name: str, p2_media_id: int | None, p2_score: int,
      code: str = uuid4(), feedback: str | None = None,
  ):
    self.p1_name = p1_name
    self.p1_media_id = p1_media_id
    self.p1_score = p1_score
    self.p2_name = p2_name
    self.p2_media_id = p2_media_id
    self.p2_score = p2_score
    self.code = code
    self.feedback = feedback

  def __repr__(self):
    return (f"DisplayRow("
            f"p1_name={self.p1_name}, p1_media_id={self.p1_media_id}, p1_score={self.p1_score}, "
            f"p2_name={self.p2_name}, p2_media_id={self.p2_media_id}, p2_score={self.p2_score}, "
            f"code={self.code}, feedback={self.feedback}"
            f")")

  @classmethod
  def from_row(cls, row: Row):
    return cls(
        p1_name=row["p1_name"],
        p1_media_id=row["p1_media_id"],
        p1_score=row["p1_score"],
        p2_name=row["p2_name"],
        p2_media_id=row["p2_media_id"],
        p2_score=row["p2_score"],
        code=row["code"],
        feedback=row["feedback"],
    )

  @classmethod
  def from_request(
      cls,
      request: Request,
      p1_media_id: int,
      p2_media_id: int
  ):
    return cls(
        p1_name=request.form.get("p1_name"),
        p1_media_id=p1_media_id,
        p1_score=request.form.get("p1_score", type=int),
        p2_name=request.form.get("p2_name"),
        p2_media_id=p2_media_id,
        p2_score=request.form.get("p2_score", type=int),
        code=str(uuid4()),
        feedback=request.form.get("feedback"),
    )
