from __main__ import app, request, User, generate_password_hash, db_session, redirect, render_template, url_for
from form.signup_form import SignUpForm

@app.route("/signup", methods = ["GET", "POST"])
def sign_up():
    signup_form = SignUpForm(request.form)
    
    if request.method == "POST" and signup_form.validate():
        new_user = User(
            signup_form.username.data,
            signup_form.email.data,
            generate_password_hash(signup_form.password.data)
        )
        db_session.add(new_user) 
        db_session.commit()
        return redirect(url_for("index"))
    return render_template("signup.html", title="sign up", form=signup_form)