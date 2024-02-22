from flask import Flask, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from utils import Session, User
app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

import routes.index
import routes.signup

@app.route("/login", methods = ["GET", "POST"])
def login(): 
    from form.login import LogInForm
    login_form = LogInForm(request.form)
    
    return redirect(url_for("/login"), title="Login", form = login_form)
    

if __name__ == "__main__":
    app.run()
