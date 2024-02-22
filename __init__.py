from flask import Flask, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from utils import Session, User

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

from form.signup import SignUpForm
@app.route("/signup", methods = ["GET", "POST"])
def sign_up():
    signup_form = SignUpForm(request.form)
    
    if request.method == "POST" and signup_form.validate():
        new_user = User(
            signup_form.username.data,
            signup_form.email.data,
            generate_password_hash(signup_form.password.data)
        )
        Session.add(new_user)
        Session.commit()
        return redirect(url_for("index"))
    return render_template("signup.html", title="sign up", form=signup_form)

@app.route("/login", methods = ["GET", "POST"])
def login(): 
    from form.login import LogInForm
    login_form = LogInForm(request.form)
    
    return redirect(url_for("/login"), title="Login", form = login_form)
    

if __name__ == "__main__":
    app.run()
