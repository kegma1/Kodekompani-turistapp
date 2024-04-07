from __main__ import app
from libs.helpers import is_logged_in, get_user_status, require_login
from db_utils import db_session, User, Friend
from flask import render_template, url_for, redirect, session

@app.route('/people/<username>', methods=["GET"])
def people_page(username: str):
    user = db_session.query(User).filter_by(username = username).first()
    
    if not user:
        return "no user by that name"
    
    following_users = db_session.query(Friend).filter_by(user_id = user.id).all()
    followers_users = db_session.query(Friend).filter_by(friend_id = user.id).all()

    top_5_achievements = None
    if user.achievements is not []:
            top_5_achievements = sorted(user.achievements, key=lambda x: x.xp_reward, reverse=True)[:5]

    user_status = get_user_status(user)

    following = False
    same_user = False
    if is_logged_in():
        current_user = db_session.query(User).filter_by(username = session["user"]).first()
        following = user in current_user.friends
        same_user = user.username == current_user.username

    return render_template("public_profile.html", 
                           title=f"{username}'s profile", 
                           user=user, 
                           logged_in=is_logged_in(),
                           t5achievements=top_5_achievements,
                           user_status = user_status,
                           following=following,
                           same_user=same_user,
                           followers_users = followers_users,
                           following_users = following_users
                           )

@app.route('/follow_user/<username>', methods=["GET"])
@require_login
def follow_user(username: str):
    current_user = db_session.query(User).filter_by(username = session["user"]).first()
    user = db_session.query(User).filter_by(username = username).first()
    current_user.friends.append(user)
    db_session.commit()
    return redirect(url_for("people_page", username = username))

@app.route('/unfollow_user/<username>', methods=["GET"])
@require_login
def unfollow_user(username: str):
    current_user = db_session.query(User).filter_by(username = session["user"]).first()
    user = db_session.query(User).filter_by(username = username).first()

    if user in current_user.friends:
        current_user.friends.remove(user)
        db_session.commit()

    return redirect(url_for("people_page", username = username))