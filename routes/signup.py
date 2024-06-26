from __main__ import app
from flask import session, redirect, render_template, url_for, request
from db_utils import User, db_session
from werkzeug.security import generate_password_hash
from form.signup_form import SignUpForm

@app.route("/signup", methods = ["GET", "POST"])
def sign_up():
    signup_form = SignUpForm(request.form)
    
    if request.method == "POST" and signup_form.validate():
        full_name = f'{signup_form.first_name.data} {signup_form.last_name.data}'
        new_user = User(
            signup_form.username.data,
            signup_form.email.data,
            generate_password_hash(signup_form.password.data),
            full_name,
            signup_form.year.data
        )
        db_session.add(new_user)
        db_session.commit()
        session["is_logged_in"] = True
        session["user"] = new_user.username
        session["admin"] = new_user.isAdmin
        
        return redirect(url_for("index"))
    return render_template("signup.html", title="sign up", form=signup_form)