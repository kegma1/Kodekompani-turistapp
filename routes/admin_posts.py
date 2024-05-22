from __main__ import app
from flask import redirect, render_template, url_for, redirect, session
from db_utils import UserPosts, db_session
from libs.helpers import require_login, require_admin, paging, get_change

@app.route("/admin_posts/<int:page>", methods = ["GET", "POST"]) 
@require_login
@require_admin
def admin_posts(page):
    data = paging(page, 5, UserPosts,)
    
    if not data and page == 1:
        return redirect(url_for("index"))
    
    elif not data:
        return redirect(url_for("admin_posts", page = 1))
    
    return render_template("admin_posts.html",
                            posts = data, 
                            page = page,
                            title = "Admin Page")

@app.route("/admin_del_post/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_post(change_id):
    post = db_session.query(UserPosts).filter_by(post_id = change_id).first()
    post.isDeleted = not post.isDeleted
    db_session.commit()
    
    return redirect(url_for("admin_posts", page = 1))

@app.route("/admin_del_post_img/<change_id>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_del_post_img(change_id):
    post = db_session.query(UserPosts).filter_by(post_id = change_id).first()
    post.image = None
    db_session.commit()
    
    return redirect(url_for("admin_posts", page = 1))


    


