from __main__ import app, request, generate_password_hash, redirect, render_template, url_for, session
from form.login_form import LogInForm
from db_utils import db_session, User
from flask import redirect, url_for

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_logged_in', None)
    session.pop('admin', None)
    return redirect(url_for('login'))
