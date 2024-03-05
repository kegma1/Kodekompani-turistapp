from __main__ import session
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session

def get_curr_user():
    return db_session.query(User).filter_by(username = session['user']).first()

def get_change_user(change_id):
    return db_session.query(User).filter_by(id = change_id).first()

def is_admin():
    return True if ("is_logged_in" in session 
                    and session["is_logged_in"] 
                    and session['admin']) else False