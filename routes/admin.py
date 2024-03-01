from __main__ import app, redirect, render_template, url_for, redirect
from flask import request
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode

@app.route("/admin", methods = ["GET", "POST"]) # Needs more checks for admin privileges in the future
def admin():
    return render_template("admin.html", 
                        friends = db_session.query(Friend).all(), 
                        users = db_session.query(User).all(), 
                        user_attractions = db_session.query(UserAttraction).all(), 
                        user_achievement = db_session.query(UserAchievement).all(),
                        title = "Admin Page")

@app.route("/admin_del_user/<id>", methods = ["GET", "POST"])
def admin_del_user(id):
    db_session.query(User).filter_by(id = id).delete()
    db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_pfp/<id>", methods = ["GET", "POST"])
def admin_del_pfp(id):
    user = db_session.query(User).filter_by(id = id).first()
    user.profile_pic = None
    db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_admin/<id>", methods = ["GET", "POST"])
def admin_del_admin(id):
    user = db_session.query(User).filter_by(id = id).first()
    user.isAdmin = not user.isAdmin
    db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_bio/<id>", methods = ["GET", "POST"])
def admin_del_bio(id):
    user = db_session.query(User).filter_by(id = id).first()
    user.bio = ""
    db_session.commit()
    
    return redirect(url_for("admin"))