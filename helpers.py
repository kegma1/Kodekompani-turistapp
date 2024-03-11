''''a module for utility functions or helper functions
'''
from functools import wraps
from flask import flash, redirect, session, url_for

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "is_logged_in" not in session or not session["is_logged_in"]:
            flash('Available only authorized users.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function