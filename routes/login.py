from __main__ import app
from form.login_form import LogInForm
from db_utils import db_session, User
from flask import request, redirect, render_template, url_for, session

@app.route("/login", methods = ["GET", "POST"])
def login(): 
    login_form = LogInForm(request.form)
    
    if request.method == "POST" and login_form.validate():

        session["is_logged_in"] = True
        session['user'] = login_form.username.data

        curr_user = db_session.query(User).filter_by(username = session['user']).first()
        session['admin'] = curr_user.isAdmin
        session['user_id'] = curr_user.id
        
        return redirect(url_for("index"))

    return render_template("login.html", title="Login", form = login_form)
