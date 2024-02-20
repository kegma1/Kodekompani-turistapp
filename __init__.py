from flask import Flask, render_template, request, url_for, session, redirect
import secrets


app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def sign_up():
    from form.signup import SignUpForm
    signup_form = SignUpForm(request.form)
    if request.method == "POST" and signup_form.validate():
        print(signup_form)

    return render_template("signup.html", title="sign up", form=signup_form)

if __name__ == "__main__":
    app.run()