''''a module for utility functions or helper functions
'''
from functools import wraps
from flask import redirect, session, url_for
from libs.admin_fn import is_admin
import datetime as buh

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