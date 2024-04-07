from __main__ import app
from flask import render_template
from db_utils import db_session, User

@app.route('/followers_list', methods=["GET"])
def followers_list(follow):
    followers = get_follow_info(follow, 'user_id')
        
    return render_template()


@app.route('/following_list', methods=["GET"])
def following_list(follow):
    following = get_follow_info(follow, 'friend_id')


def get_follow_info(follow, id):
    for _ in follow:
        x = db_session.query(User).filter_by(id = id).all()
    return x