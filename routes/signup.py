from __main__ import app, request, User, generate_password_hash, Session, redirect, render_template, url_for
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