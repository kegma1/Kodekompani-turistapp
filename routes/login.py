from __main__ import app, request, User, generate_password_hash, Session, redirect, render_template, url_for
from form.login_form import LogInForm

@app.route("/login", methods = ["GET", "POST"])
def login(): 
    login_form = LogInForm(request.form)
    
    return render_template("login.html", title="Login", form = login_form)