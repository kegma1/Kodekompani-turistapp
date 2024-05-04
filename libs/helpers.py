''''a module for utility functions or helper functions
'''
from functools import wraps
from flask import redirect, session, url_for, request
import datetime as buh
from db_utils import db_session, User

#STANDARDIZED AGE GROUPS
age_groups = [0, 1, 3, 6, 9, 13, 18]

def is_logged_in():
    return "is_logged_in" in session and session["is_logged_in"]

def get_change(change_id):
    return db_session.query(User).filter_by(id = change_id).first()

def is_admin():
    return (is_logged_in() and "admin" in session and session['admin'])


def get_user_status(user):
    xp = user.xp_collected
    xp = 0 if xp == None else xp
    if xp < 100: user_status = "Newbie in city"
    elif xp < 500: user_status = "Tourist"
    elif xp < 1000: user_status = "Svarta bjorn"
    else: user_status = "Rallar"

    return user_status


def get_user_age(user):
    birth = user.age
    curr_date = buh.date.today()
    age = curr_date.year - birth.year
    
    return age if (curr_date.month, curr_date.day) >= (birth.month, birth.day) else age - 1

def get_curr_user():
    return db_session.query(User).filter_by(username = session['user']).first()

def paging(page: int, amount: int, table = None, filter_deleted = False, query = None): #KOTLIN PILLED RAHHH
    '''
    Divides up the page (int) into amount (int) elements desplayed.
    If there are no elements in the given page, return None.
    Returns data (list) given the page and amount parameters if elements are in page.
    ''' 
    if page < 1:
        return None
    
    if filter_deleted:
        data = db_session.query(table).filter(table.isDeleted == False).offset((page * amount) - amount).limit(amount).all()
    elif query is not None:
        data = query.offset((page * amount) - amount).limit(amount).all()
    else:
        data = db_session.query(table).offset((page * amount) - amount).limit(amount).all()

    if not data and page != 1:
        return None
    return data


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "is_logged_in" not in session or not session["is_logged_in"]:
            session["next"] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            return redirect(url_for('funi', id = 1))
        return f(*args, **kwargs)
    return decorated_function 

def is_mobile(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_agent = request.headers.get('User-Agent').lower()
        kwargs['is_mobile'] = 'mobi' in user_agent or 'iphone' in user_agent or 'android' in user_agent
        return f(*args, **kwargs)
    return decorated_function