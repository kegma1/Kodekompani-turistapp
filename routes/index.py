from __main__ import app
from flask import render_template, session, redirect, url_for, request
from db_utils import db_session, User, Attraction, UserPosts
from libs.helpers import get_curr_user, get_user_age, is_logged_in
from libs.create_post import create_post
from form.post_form import PostForm
from werkzeug.datastructures import CombinedMultiDict

@app.route("/", methods = ["GET", "POST"])
def index():
    pfp = None
    bio = None
    username = ""
    fullname = ""
    attractions = []
    xp = 0; user_status = "Newbie in city"
    post_form = None
    posts = None

    top_5_achievements = None
    
    # fetch attractions for all visitors
    attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= 0).all()

    if is_logged_in():
        data = db_session.query(User).filter_by(username=session["user"]).first()
        bio = data.bio
        post_form = PostForm(None, formdata=CombinedMultiDict((request.files, request.form)))
        
        user = get_curr_user()

        if data.profile_pic:
            pfp = data.profile_pic

        username = session["user"]
        fullname = data.full_name

        # Finding top 5 achievements
        if data.achievements is not []:
            top_5_achievements = sorted(data.achievements, key=lambda x: x.xp_reward, reverse=True)[:5]
            
        age = get_user_age(data)

        attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= age).all()

        posts_raw = db_session.query(UserPosts)\
                .join(UserPosts.user)\
                .filter(User.followers.any(User.id == user.id))\
                .filter(UserPosts.isDeleted == False)\
                .filter(User.isDeleted == False).all()
        
        posts = sorted(posts_raw, key=lambda x: x.time, reverse=True)

    if is_logged_in() and request.method == "POST" and post_form.validate_on_submit():
        create_post(post_form.attraction.data, post_form.message.data, post_form.image.data)
        return redirect(url_for("index"))

    return render_template("index.html", 
                           title = "Home page", 
                           pfp = pfp, 
                           bio = bio or None,  
                           username = username, 
                           xp = xp, 
                           fullname = fullname, 
                           attractions = attractions,
                           t5achievements = top_5_achievements,
                           post_form=post_form,
                           posts= posts)
