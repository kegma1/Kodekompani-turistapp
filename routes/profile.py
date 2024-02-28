from __main__ import app
from flask import request,  redirect, render_template, url_for, session
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from werkzeug.security import generate_password_hash
from form.profile_form import ProfileForm
from PIL import Image
from io import BytesIO
from base64 import b64encode
from libs.pfp import make_profile

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    profile_form = ProfileForm(request.form)
    info = db_session.query(User).filter_by(username = session['user']).first()

    profile_picture = b64encode(info.profile_pic).decode("utf-8")


    if request.method == "POST" and profile_form.validate():
        info.username = profile_form.username.data
        session['user'] = profile_form.username.data
        info.email = profile_form.email.data
        full_name = f'{profile_form.first_name.data} {profile_form.last_name.data}'
        info.full_name = full_name

        if "picture" in request.files and request.files["picture"] and not profile_form.keep_picture.data:
            
            buffer = BytesIO()
            image = Image.open(request.files["picture"].stream)
            image = image.resize((200, 200))
            
            image.save(buffer, format="PNG", quality=20, optimize=True)

            buffer.seek(0)
            info.profile_pic = buffer.read()
        elif profile_form.keep_picture.data:
            default_picture = make_profile(info.username, 200, 50)
            info.profile_pic = default_picture.read()

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
    return render_template("profile.html", title="Edit Profile", form = profile_form, username = info.username, email = info.email, profile_picture = profile_picture)
    