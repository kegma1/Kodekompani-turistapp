from __main__ import app, request, User, generate_password_hash, db_session, redirect, render_template, url_for, session
from utils import Friend, User, UserAttraction, UserAchievement, db_session
from form.profile_form import ProfileForm

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    profile_form = ProfileForm(request.form)
    info = db_session.query(User).filter_by(username = session['user']).first()

    if request.method == "POST" and profile_form.validate():
        info.username = profile_form.username.data
        session['user'] = profile_form.username.data
        info.email = profile_form.email.data
        db_session.commit()

        return redirect(url_for("index"))

    print('TEST RESULT')    
    print(info.username, info.email)
    profile_form.add_placeholder("username", info.username)
    profile_form.add_placeholder("email", info.email)
    return render_template("profile.html", title="Edit Profile", form = profile_form, username = info.username, email = info.email)
    