''''a module for utility functions or helper functions
'''
from functools import wraps
from flask import redirect, session, url_for
from libs.admin_fn import is_admin

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
            return redirect(url_for('funi'))
        return f(*args, **kwargs)
    return decorated_function