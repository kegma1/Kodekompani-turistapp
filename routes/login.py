from __main__ import app, request, generate_password_hash, redirect, render_template, url_for
from form.login_form import LogInForm
from utils import Session, User

@app.route("/login", methods = ["GET", "POST"])
def login(): 
    login_form = LogInForm(request.form)
    
    if request.method == "POST" and login_form.validate():
        return redirect(url_for("index"))

    
    return render_template("login.html", title="Login", form = login_form)