''''a module for utility functions or helper functions
'''
from functools import wraps
from flask import redirect, session, url_for, render_template
from libs.admin_fn import is_admin
import datetime as buh
from db_utils import db_session
from routes import *

def is_logged_in():
    return "is_logged_in" in session and session["is_logged_in"]


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


def paging(page: int, amount: int, table): #KOTLIN PILLED RAHHH
    '''
    Divides up the page (int) into amount (int) elements desplayed.
    If there are no elements in the given page, return None.
    Returns data (list) given the page and amount parameters if elements are in page.
    ''' 
    if page < 1:
        return None
    
    data = db_session.query(table).offset((page * amount) - amount).limit(amount).all()
    
    if not data and page != 1:
        return None
    return data


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "is_logged_in" not in session or not session["is_logged_in"]:
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