from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode
from helpers import require_login
from libs.admin_fn import is_admin, get_curr_user, get_change_user

# Needs more checks for admin privileges in the future
@app.route("/admin", methods = ["GET", "POST"]) 
@require_login
def admin():
    if is_admin():
        return render_template("admin.html", 
                            friends = db_session.query(Friend).all(), 
                            users = db_session.query(User).all(), 
                            user_attractions = db_session.query(UserAttraction).all(), 
                            user_achievement = db_session.query(UserAchievement).all(),
                            title = "Admin Page")
    return redirect(url_for("funi"))

@app.route("/admin_del_user/<change_id>", methods = ["GET", "POST"])
def admin_del_user(change_id):
    if is_admin():
        curr_user = get_curr_user()
        
        # FIX YO
        if curr_user.id == change_id:
            db_session.query(User).filter_by(id = change_id).delete()
            db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))

@app.route("/admin_del_pfp/<change_id>", methods = ["GET", "POST"])
def admin_del_pfp(change_id):
    if is_admin():
        user = get_change_user(change_id)
        user.profile_pic = None
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))

@app.route("/admin_del_admin/<change_id>", methods = ["GET", "POST"])
def admin_del_admin(change_id):
    if is_admin():
        change = get_change_user(change_id)
        change.isAdmin = not change.isAdmin

        if session['user'] == change.username:
            session['admin'] = change.isAdmin
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))

@app.route("/admin_del_bio/<change_id>", methods = ["GET", "POST"])
def admin_del_bio(change_id):
    if is_admin():
        user = get_change_user(change_id)
        user.bio = ""
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))
    
@app.route("/funi")
def funi():
    return render_template("iocularis.html")
        