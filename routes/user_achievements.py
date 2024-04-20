# routes/user_achievements.py
from flask import render_template
from db_utils import db_session, Achievement
from libs.helpers import require_login, get_curr_user

from __main__ import app

@require_login
@app.route('/user_achievements')
def user_achievements():
    user = get_curr_user()
    
    all_achievements = db_session.query(Achievement).all()
    completed_achievements_ids = {achievement.id for achievement in user.achievements}

    return render_template('user_achievements.html', 
                           all_achievements=all_achievements, 
                           completed_achievements_ids=completed_achievements_ids)
