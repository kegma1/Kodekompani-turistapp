from __main__ import session
from db_utils import db_session

#STANDARDIZED AGE GROUPS
age_groups = [0, 1, 3, 6, 9, 13, 18]

def get_curr(table):
    return db_session.query(table).filter_by(username = session['user']).first()

def get_change(table, change_id):
    return db_session.query(table).filter_by(id = change_id).first()

def is_admin():
    return True if ("is_logged_in" in session 
                    and session["is_logged_in"] 
                    and session['admin']) else False