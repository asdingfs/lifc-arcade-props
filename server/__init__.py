import os
from flask import Flask, render_template, request, redirect, url_for, flash
from . import db
from werkzeug.utils import secure_filename
import sqlite3
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'server.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # setup database
    db.init_app(app)

    @app.route("/")
    def index():
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute('''SELECT d.*, m1.url as p1ImgSrc, m2.url as p2ImgSrc FROM display d
                       LEFT JOIN media m1 ON d.p1_media_id = m1.id
                       LEFT JOIN media m2 ON d.p2_media_id = m2.id
                       ORDER BY d.created_at DESC''')
        entries = cur.fetchall()
        db.close()
        return render_template("index.html", entries=entries)

    @app.route("/create", methods=["GET", "POST"])
    def create():
        if request.method == "POST":
            p1_name = request.form.get("p1_name")
            p2_name = request.form.get("p2_name")
            p1_score = request.form.get("p1_score")
            p2_score = request.form.get("p2_score")
            code = request.form.get("code")
            code = str(uuid.uuid4())
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
                cur.execute("INSERT INTO media (url) VALUES (?)", (f"uploads/{filename}",))
                p1_media_id = cur.lastrowid
            # Handle p2 image
            if p2_img and allowed_file(p2_img.filename):
                filename = secure_filename(p2_img.filename)
                p2_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("INSERT INTO media (url) VALUES (?)", (f"uploads/{filename}",))
                p2_media_id = cur.lastrowid
            cur.execute('''INSERT INTO display (p1_name, p1_media_id, p1_score, p2_name, p2_media_id, p2_score, code, feedback) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (p1_name, p1_media_id, p1_score, p2_name, p2_media_id, p2_score, code, feedback))
            db.commit()
            db.close()
            flash("Entry created successfully!", "success")
            return redirect(url_for("index"))
        return render_template("create.html")

    return app
