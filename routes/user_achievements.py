# routes/user_achievements.py
from flask import render_template, session, redirect, url_for
from db_utils import db_session, Achievement, User

from __main__ import app

@app.route('/user_achievements')
def user_achievements():
    user_id = session.get('user_id')
    
    if user_id is None:
        return redirect(url_for('login'))
    
    user = db_session.query(User).filter_by(id=user_id).first()

    if not user:
        return render_template('error.html', message="User not found.")
    
    all_achievements = db_session.query(Achievement).all()
    completed_achievements_ids = {achievement.id for achievement in user.achievements}

    return render_template('user_achievements.html', 
                           all_achievements=all_achievements, 
                           completed_achievements_ids=completed_achievements_ids)
