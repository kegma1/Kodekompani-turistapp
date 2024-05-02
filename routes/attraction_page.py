from __main__ import app
from flask import render_template, request, redirect, url_for, session
from db_utils import db_session, Attraction, User, Achievement, UserAchievement, UserPosts
from libs.helpers import require_login, get_user_age
from form.passcode_form import Passcode
from form.post_form import PostForm
from libs.create_post import create_post
from werkzeug.datastructures import CombinedMultiDict

@app.route('/attraction/<attraction_id>', methods=["GET", "POST"])
@require_login
def view_attraction(attraction_id: int):
    attraction_info = db_session.query(Attraction).filter_by(id=attraction_id).first()
    user = db_session.query(User).filter_by(username = session["user"]).first()
    posts = db_session.query(UserPosts).filter_by(attraction_id = attraction_id, is_status = False).all()
    
    age = get_user_age(user)
    attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= age).all()
    if attraction_info not in attractions:
        return redirect(url_for("index"))
    
    passcode_form = Passcode(attraction_id, request.form)
    post_form = PostForm(attraction_id, formdata=CombinedMultiDict((request.files, request.form)))

    user_achivements = db_session.query(Achievement).join(UserAchievement).filter(
        UserAchievement.user_id == user.id,
        Achievement.attraction_id == attraction_id
    ).all()

    coords = attraction_info.location_coordinates.split(",")
    assert len(coords) == 2


    if request.method == "POST" and passcode_form.validate():
        return redirect(url_for("unlock_achivement", attraction = attraction_id, passcode = passcode_form.passcode.data))

    if request.method == "POST" and post_form.validate():
        create_post(attraction_id, post_form.message.data, post_form.image.data)
        return redirect(url_for("view_attraction", attraction_id=attraction_id))

    return render_template("attraction_page.html", 
                           title=attraction_info.name, 
                           info=attraction_info, 
                           image=attraction_info.image, 
                           passcode_form=passcode_form,
                           post_form=post_form,
                           posts=posts,
                           achievements=None if not user_achivements else user_achivements,
                           lon=coords[1],
                           lat=coords[0],
                           zoom = 15
                           )