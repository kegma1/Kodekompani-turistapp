from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode
from libs.helpers import require_login, require_admin
from libs.admin_fn import is_admin, get_curr_user, get_change_user

# Needs more checks for admin privileges in the future
@app.route("/admin", methods = ["GET", "POST"]) 
@require_login
@require_admin
def admin():
    return render_template("admin.html", 
                            friends = db_session.query(Friend).all(), 
                            users = db_session.query(User).all(), 
                            user_attractions = db_session.query(UserAttraction).all(), 
                            user_achievement = db_session.query(UserAchievement).all(),
                            title = "Admin Page")

@app.route("/admin_del_user/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_user(change_id):
    change = get_change_user(change_id)

    if session['user'] != change.username:
        change.isDeleted = not change.isDeleted
        db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_pfp/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_pfp(change_id):
    user = get_change_user(change_id)
    user.profile_pic = None
    db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_admin/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_admin(change_id):
    change = get_change_user(change_id)
    curr = get_curr_user()
    admins = db_session.query(User).filter_by(isAdmin = True).all()
    
    if len(admins) > 1:
        if session['user'] != change.username:
            change.isAdmin = not change.isAdmin
            db_session.commit()
    else:
        if session['user'] != change.username and change.isAdmin == False and curr.isAdmin == True:
            change.isAdmin = True
            db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_bio/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_bio(change_id):
    user = get_change_user(change_id)
    user.bio = ""
    db_session.commit()
    
    return redirect(url_for("admin"))
    
@app.route("/funi")
def funi():
    return render_template("iocularis.html")
        