from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode
from libs.helpers import require_admin, require_login

@app.route("/admin_sights")
@require_login
@require_admin
def sights():
    return render_template("admin_sights.html")