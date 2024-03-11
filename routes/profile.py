from __main__ import app
from flask import request,  redirect, render_template, url_for, session
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from werkzeug.security import generate_password_hash
from form.profile_form import ProfileForm
from helpers import require_login

@app.route("/profile", methods = ["GET", "POST"])
@require_login
def profile():
    profile_form = ProfileForm(request.form)
    info = db_session.query(User).filter_by(username = session['user']).first()

    if request.method == "POST" and profile_form.validate():
        info.username = profile_form.username.data
        session['user'] = profile_form.username.data
        info.email = profile_form.email.data
        info.full_name = f'{profile_form.first_name.data} {profile_form.last_name.data}'

        if "picture" in request.files and request.files["picture"] and not profile_form.keep_picture.data:
            info.profile_pic = request.files["picture"].stream
        elif profile_form.keep_picture.data:
            info.profile_pic = None

        info.bio = profile_form.bio.data
        db_session.commit()

        return redirect(url_for("index"))

    fullName = info.full_name.split()
    first_name = fullName[0]
    last_name = fullName[1]
    profile_form.username.data = info.username
    profile_form.first_name.data = first_name
    profile_form.last_name.data = last_name
    profile_form.email.data = info.email
    profile_form.year.data = info.age
    profile_form.bio.data = info.bio
    return render_template("profile.html", title="Edit Profile", form = profile_form, username = info.username, email = info.email, profile_picture = info.profile_pic)
    