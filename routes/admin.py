from __main__ import app
from flask import redirect, render_template, url_for, redirect, session
from db_utils import User, db_session, func
from libs.helpers import require_login, require_admin
from libs.admin_fn import get_curr, get_change

# Needs more checks for admin privileges in the future
@app.route("/admin/<page>", methods = ["GET", "POST"]) 
@require_login
@require_admin
def admin(page):
    page = int(page)
    users = []
    
    for i in range(page*8 - 8, page*8):
        user = db_session.query(User).filter_by(id = i).first()
        
        if user != None:
            users.append(user)
            
    if users == [] and db_session.query(func.count(User.id)).scalar() != 0:
        return redirect(url_for("admin", page = 1))
    
    return render_template("admin.html",
                            users = users, 
                            page = page,
                            title = "Admin Page")

@app.route("/admin_del_user/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_user(change_id):
    change = get_change(User ,change_id)

    if session['user'] != change.username:
        change.isDeleted = not change.isDeleted
        db_session.commit()
    
    return redirect(url_for("admin", page = 1))

@app.route("/admin_del_pfp/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_pfp(change_id):
    user = get_change(User, change_id)
    user.profile_pic = None
    db_session.commit()
    
    return redirect(url_for("admin", page = 1))

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
    
    return redirect(url_for("admin", page = 1))

@app.route("/admin_del_bio/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_bio(change_id):
    user = get_change(User, change_id)
    user.bio = ""
    db_session.commit()
    
    return redirect(url_for("admin", page = 1))
    
@app.route("/funi")
def funi():
    return render_template("iocularis.html")

