from __main__ import app, request, User, generate_password_hash, db_session, redirect, render_template, url_for
from utils import Friend, User, UserAttraction, UserAchievement, db_session
from form.profile_form import ProfileForm

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    profile_form = ProfileForm(request.form)

    return render_template("profile.html", title="Edit Profile", form = profile_form)
    