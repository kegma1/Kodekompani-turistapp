from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Attraction, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode
from libs.helpers import require_admin, require_login

@app.route("/admin_sights_edit_<id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_sights_edit(edit_id):
    return render_template("admin_sights_edit.html",
                           attraction = db_session.query(Attraction).filter_by(id = edit_id).all(),
                           title = "Admin sights edit")