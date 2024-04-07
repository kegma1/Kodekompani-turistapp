from __main__ import app
from flask import render_template, redirect, url_for
from db_utils import db_session, User

@app.route('/followers_list/<userid>', methods=["GET"])
def followers_list(userid):
    urlname = 'followers_list'
    # page = int(page)
    # if page < 1:
    #     return redirect(url_for("followers_list", userid = userid, page = 1))
    
    user = db_session.query(User).filter_by(id = userid).first()

    # if not user and page != 1:
    #     return redirect(url_for("followers_list", userid = userid, page = 1))
    
    return render_template("follow_list.html", userlist = user.followers, previoususer = user, urlname = urlname)


@app.route('/following_list/<userid>', methods=["GET"])
def following_list(userid):
    urlname = 'following_list'
    # page = int(page)
    # if page < 1:
    #     return redirect(url_for("following_list", userid = userid, page = 1))
    
    user = db_session.query(User).filter_by(id = userid).first()

    # if not user and page != 1:
    #     return redirect(url_for("following_list", userid = userid, page = 1))
    
    return render_template("follow_list.html", userlist = user.following, previoususer = user, urlname = urlname)

# def get_follow_info(follow, id):
#     for _ in follow:
#         x = db_session.query(User).filter_by(id = id).all()
#     return x