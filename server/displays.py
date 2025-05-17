from flask import Blueprint, render_template, request, redirect, url_for, abort, \
  flash, current_app
from flask_htmx import HTMX
from server.db import get_db
from server.utils import allowed_file
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import sqlite3

bp = Blueprint("displays", __name__, url_prefix="/displays")
app = current_app


@bp.route("/", methods=["GET"])
def list_displays():
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
      '''
                  SELECT d.*, m1.url as p1ImgSrc, m2.url as p2ImgSrc 
                  FROM display d
                  LEFT JOIN media m1 ON d.p1_media_id = m1.id
                  LEFT JOIN media m2 ON d.p2_media_id = m2.id
                  ORDER BY d.created_at DESC
              '''
  )
  entries = cursor.fetchall()
  db.close()
  return render_template("partials/displays/_index.html.j2", entries=entries)


@bp.route("/create", methods=["GET", "POST"])
def create_display():
  if request.method == "POST":
    p1_name = request.form.get("p1_name")
    p2_name = request.form.get("p2_name")
    p1_score = request.form.get("p1_score")
    p2_score = request.form.get("p2_score")
    code = str(uuid4())
    feedback = request.form.get("feedback")
    p1_img = request.files.get("p1ImgSrc")
    p2_img = request.files.get("p2ImgSrc")
    db = sqlite3.connect(app.config['DATABASE'])
    cur = db.cursor()
    p1_media_id = None
    p2_media_id = None
    # Handle p1 image
    if p1_img and allowed_file(p1_img.filename):
      filename = secure_filename(p1_img.filename)
      p1_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      cur.execute(
          "INSERT INTO media (url) VALUES (?)",
          (f"uploads/{filename}",)
      )
      p1_media_id = cur.lastrowid
    # Handle p2 image
    if p2_img and allowed_file(p2_img.filename):
      filename = secure_filename(p2_img.filename)
      p2_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      cur.execute(
          "INSERT INTO media (url) VALUES (?)",
          (f"uploads/{filename}",)
      )
      p2_media_id = cur.lastrowid
    cur.execute(
        '''INSERT INTO display (p1_name, p1_media_id, p1_score, p2_name, p2_media_id, p2_score, code, feedback) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (p1_name, p1_media_id, p1_score, p2_name, p2_media_id, p2_score,
         code, feedback)
    )
    db.commit()
    db.close()
    flash("Entry created successfully!", "success")
    return redirect(url_for("index"))
  return render_template("partials/displays/_create.html.j2")
