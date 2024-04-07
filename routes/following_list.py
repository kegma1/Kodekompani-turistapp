from __main__ import app
from flask import render_template
from db_utils import db_session, User

@app.route('/followers_list/<userid>', methods=["GET"])
def followers_list(userid):
    user = db_session.query(User).filter_by(id = userid).first()
    return render_template("follow_list.html", userlist = user.followers, previoususer = user.username)


@app.route('/following_list/<userid>', methods=["GET"])
def following_list(userid):
    user = db_session.query(User).filter_by(id = userid).first()
    return render_template("follow_list.html", userlist = user.following, previoususer = user.username)

# def get_follow_info(follow, id):
#     for _ in follow:
#         x = db_session.query(User).filter_by(id = id).all()
#     return x