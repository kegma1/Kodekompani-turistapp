from __main__ import app
from flask import redirect, render_template, url_for, redirect, session
from db_utils import User, db_session
from libs.helpers import require_login, require_admin, paging, get_curr_user, get_change

# Needs more checks for admin privileges in the future
@app.route("/admin/<int:page>", methods = ["GET", "POST"]) 
@require_login
@require_admin
def admin(page):
    data = paging(page, 5, User)
    
    if not data:
        return redirect(url_for("admin", page = 1))
    
    return render_template("admin.html",
                            users = data, 
                            page = page,
                            title = "Admin Page")

@app.route("/admin_del_user/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_user(change_id):
    change = get_change(change_id)

    if session['user'] != change.username:
        change.isDeleted = not change.isDeleted
        db_session.commit()
    
    return redirect(url_for("admin", page = 1))

@app.route("/admin_del_pfp/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_pfp(change_id):
    user = get_change(change_id)
    user.profile_pic = None
    db_session.commit()
    
    return redirect(url_for("admin", page = 1))

@app.route("/admin_del_admin/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_admin(change_id):
    change = get_change(change_id)
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
    
    return redirect(url_for("admin", page = 1))

@app.route("/admin_del_bio/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_bio(change_id):
    user = get_change(change_id)
    user.bio = ""
    db_session.commit()
    
    return redirect(url_for("admin", page = 1))
    
@app.route("/video/<int:id>")
def funi(id):
    video = ["https://player.vimeo.com/video/794492622?h=31cc9f209b&autoplay=1&loop=1",
             "https://www.youtube.com/embed/oW3B34D0RVk?si=FiTBZPdp6dOMviY4"]
    try:
        show = video[id - 1]
    except:
        show = video[0]
    
    return render_template("iocularis.html", embed = show)

