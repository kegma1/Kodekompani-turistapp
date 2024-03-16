from __main__ import app, redirect, render_template, url_for, redirect, session
from flask import request
from db_utils import Attraction, User, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode
from libs.helpers import require_login, require_admin
from libs.admin_fn import is_admin, get_curr, get_change

# Needs more checks for admin privileges in the future
@app.route("/admin", methods = ["GET", "POST"]) 
@require_login
@require_admin
def admin():
    return render_template("admin.html",
                            users = db_session.query(User).all(), 
                            title = "Admin Page")

@app.route("/admin_del_user/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_user(change_id):
    change = get_change(User ,change_id)

    if session['user'] != change.username:
        change.isDeleted = not change.isDeleted
        db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_pfp/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_pfp(change_id):
    user = get_change(User, change_id)
    user.profile_pic = None
    db_session.commit()
    
    return redirect(url_for("admin"))

@app.route("/admin_del_admin/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_admin(change_id):
    change = get_change(User, change_id)
    curr = get_curr(User)
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
    user = get_change(User, change_id)
    user.bio = ""
    db_session.commit()
    
    return redirect(url_for("admin"))
    
@app.route("/funi")
def funi():
    return render_template("iocularis.html")
        
@app.route("/add_attraction", methods=["GET", "POST"])
@require_login
@require_admin
def add_attraction():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")
        age_recommendation = request.form.get("age_recommendation")
        location_coordinates = request.form.get("location_coordinates")
        address = request.form.get("address")
        group = request.form.get("group")
        keywords = request.form.get("keywords")

        new_attraction = Attraction(name=name, description=description, category=category, 
                                    age_recommendation=age_recommendation, location_coordinates=location_coordinates, 
                                    address=address, group=group, keywords=keywords)
        db_session.add(new_attraction)
        db_session.commit()

        return redirect(url_for("admin_sights"))

    return render_template("add_attraction.html")
