from __main__ import app
from flask import session, redirect, url_for
from db_utils import db_session, Achievement, User
from libs.helpers import require_login

@app.route("/unlock_achivement/attr=<attraction>pass=<passcode>", methods=["GET"])
@require_login
def unlock_achivement(attraction: int, passcode: str):
    user = db_session.query(User).filter_by(username=session["user"]).first()
    achievement = db_session.query(Achievement).filter_by(pass_code=passcode, attraction_id=attraction).first()
     
    if achievement and achievement not in user.achievements:
        if user.xp_collected:
            user.xp_collected += achievement.xp_reward
        else:
            user.xp_collected = achievement.xp_reward
        user.achievements.append(achievement)
        
        if achievement.attraction not in user.attractions:
            user.attractions.append(achievement.attraction)
    
        db_session.commit()
    
    return redirect(url_for("view_attraction", attraction_id = attraction))
