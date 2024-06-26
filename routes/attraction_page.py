from __main__ import app
from flask import render_template, request, redirect, url_for, session
from db_utils import db_session, Attraction, User, Achievement, UserAchievement, UserPosts
from libs.helpers import require_login, get_user_age, is_local_admin, is_admin, is_mobile
from form.passcode_form import Passcode
from form.post_form import PostForm
from libs.create_post import create_post
from werkzeug.datastructures import CombinedMultiDict

@app.route('/attraction/<attraction_id>', methods=["GET", "POST"])
@require_login
@is_mobile
def view_attraction(attraction_id: int, is_mobile):
    attraction_info = db_session.query(Attraction).filter_by(id=attraction_id).first()
    if attraction_info.isDeleted:
        return redirect(url_for("attractions_list"))
    
    user = db_session.query(User).filter_by(username = session["user"]).first()
    posts_raw = db_session.query(UserPosts).join(UserPosts.user)\
        .filter(UserPosts.attraction_id == attraction_id)\
        .filter(UserPosts.is_status == False, UserPosts.isDeleted == False)\
        .filter(User.isDeleted == False).all()
    
    posts = sorted(posts_raw, key=lambda x: x.post_id, reverse=True)
    
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
                           zoom = 15,
                           attraction_id = attraction_id,
                           show_edit=is_admin() or is_local_admin(attraction_id),
                           is_mobile = is_mobile
                           )