from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode

@app.route("/admin", methods = ["GET", "POST"]) # Needs more checks for admin privileges in the future
def admin():
    if is_admin():
        return render_template("admin.html", 
                            friends = db_session.query(Friend).all(), 
                            users = db_session.query(User).all(), 
                            user_attractions = db_session.query(UserAttraction).all(), 
                            user_achievement = db_session.query(UserAchievement).all(),
                            title = "Admin Page")
    return redirect(url_for("funi"))

@app.route("/admin_del_user/<id>", methods = ["GET", "POST"])
def admin_del_user(id):
    if is_admin():
        db_session.query(User).filter_by(id = id).delete()
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))

@app.route("/admin_del_pfp/<id>", methods = ["GET", "POST"])
def admin_del_pfp(id):
    if is_admin():
        user = db_session.query(User).filter_by(id = id).first()
        user.profile_pic = None
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))

@app.route("/admin_del_admin/<id>", methods = ["GET", "POST"])
def admin_del_admin(id):
    if is_admin():
        user = db_session.query(User).filter_by(id = id).first()
        user.isAdmin = not user.isAdmin
        session['user'] = user.isAdmin
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))

@app.route("/admin_del_bio/<id>", methods = ["GET", "POST"])
def admin_del_bio(id):
    if is_admin():
        user = db_session.query(User).filter_by(id = id).first()
        user.bio = ""
        db_session.commit()
        
        return redirect(url_for("admin"))
    return redirect(url_for("funi"))
    
@app.route("/funi")
def funi():
    return render_template("funi.html")

def is_admin():
    return True if ("is_logged_in" in session 
                    and session["is_logged_in"] 
                    and session['admin'] == 1) else False

        