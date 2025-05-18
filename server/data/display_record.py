from flask import Request
from server.utils import random_uuid


class DisplayRecord:
  def __init__(
      self,
      p1_name: str, p1_media_id: int | None, p1_score: int,
      p2_name: str, p2_media_id: int | None, p2_score: int,
      code: str = random_uuid(), feedback: str | None = None,
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
  def from_request(
      cls,
      request: Request,
      custom_code: str | None = None,
  ):
    return cls(
        p1_name=request.form.get("p1_name"),
        p1_media_id=request.form.get("p1_media_id", type=int),
        p1_score=request.form.get("p1_score", type=int),
        p2_name=request.form.get("p2_name"),
        p2_media_id=request.form.get("p2_media_id", type=int),
        p2_score=request.form.get("p2_score", type=int),
        code=request.form.get("code") if custom_code is None else custom_code,
        feedback=request.form.get("feedback"),
    )
