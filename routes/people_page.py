from __main__ import app
from libs.helpers import is_logged_in, get_user_status, require_login
from db_utils import db_session, User, UserPosts
from flask import render_template, url_for, redirect, session

@app.route('/people/<username>', methods=["GET"])
def people_page(username: str):
    user = db_session.query(User).filter_by(username = username).first()
    if user.isDeleted:
        return redirect(url_for("people_list", page = 1))
    
    posts_raw = db_session.query(UserPosts).filter_by(user = user, isDeleted = False).all()
    posts = sorted(posts_raw, key=lambda x: x.time, reverse=True)
    
    if not user:
        return "no user by that name"

    top_5_achievements = None
    if user.achievements is not []:
            top_5_achievements = sorted(user.achievements, key=lambda x: x.xp_reward, reverse=True)[:5]

    user_status = get_user_status(user)

    following = False
    same_user = False
    if is_logged_in():
        current_user = db_session.query(User).filter_by(username = session["user"]).first()
        following = user in current_user.following
        same_user = user.username == current_user.username

    number_of_followers = len([user for user in user.followers if not user.isDeleted])
    number_of_following = len([user for user in user.following if not user.isDeleted])

    return render_template("public_profile.html", 
                           title=f"{username}'s profile", 
                           user=user, 
                           logged_in=is_logged_in(),
                           t5achievements=top_5_achievements,
                           user_status = user_status,
                           following=following,
                           same_user=same_user,
                           posts=posts,
                           number_of_followers = number_of_followers,
                           number_of_following = number_of_following,
                           )

@app.route('/follow_user/<username>', methods=["GET"])
@require_login
def follow_user(username: str):
    current_user = db_session.query(User).filter_by(username = session["user"]).first()
    user = db_session.query(User).filter_by(username = username).first()
    current_user.following.append(user)
    db_session.commit()
    return redirect(url_for("people_page", username = username))

@app.route('/unfollow_user/<username>', methods=["GET"])
@require_login
def unfollow_user(username: str):
    current_user = db_session.query(User).filter_by(username = session["user"]).first()
    user = db_session.query(User).filter_by(username = username).first()

    if user in current_user.following:
        current_user.following.remove(user)
        db_session.commit()

    return redirect(url_for("people_page", username = username))