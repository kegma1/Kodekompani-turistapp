from __main__ import app
from flask import session, redirect, url_for
from db_utils import db_session, Achievement, User, Attraction
from libs.helpers import require_login
from libs.create_post import create_post

@app.route("/unlock_achivement/attr=<attraction>pass=<passcode>", methods=["GET"])
@require_login
def unlock_achivement(attraction: int, passcode: str):
    user = db_session.query(User).filter_by(username=session["user"]).first()
    achievement = db_session.query(Achievement).filter_by(pass_code=passcode, attraction_id=attraction).first()
    (attraction_name,) = db_session.query(Attraction.name).filter_by(id = attraction).first()
     
    if achievement and achievement not in user.achievements and not achievement.is_deleted:
        if achievement.attraction not in user.attractions:
            user.attractions.append(achievement.attraction)
            create_post(attraction, f"{session['user']} visitied {attraction_name} for the first time.", is_status=True)
        
        if user.xp_collected:
            user.xp_collected += achievement.xp_reward
        else:
            user.xp_collected = achievement.xp_reward
        create_post(attraction, f"{session['user']} collected '{achievement.name}' and earned {achievement.xp_reward}XP.", is_status=True)
        user.achievements.append(achievement)
    
        db_session.commit()
    
    return redirect(url_for("view_attraction", attraction_id = attraction))
