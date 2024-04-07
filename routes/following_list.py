from __main__ import app
from flask import render_template
from db_utils import db_session, User

@app.route('/following_list', methods=["GET"])
def follow_list(list_o_follow, friend_or_foe):
    if friend_or_foe:
        friends = get_user_info(list_o_follow, 'user_id')
    else:
       friends = get_user_info(list_o_follow, 'friend_id')
        
    return render_template()

def get_user_info(list, y):
    for x in list:
        user = db_session.query(User).filter_by(id = x.y).all()
    return user

        



