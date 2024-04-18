from __main__ import app
from flask import redirect, url_for, session

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_logged_in', None)
    session.pop('admin', None)
    return redirect(url_for('index'))
