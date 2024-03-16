from __main__ import app
from flask import render_template, request, redirect, url_for, session
from db_utils import db_session, Attraction, User, Achievement, UserAchievement
from libs.helpers import require_login
from form.passcode_form import Passcode

@app.route('/attraction/<attraction_id>', methods=["GET", "POST"])
@require_login
def view_attraction(attraction_id: int):
    passcode_form = Passcode(attraction_id, request.form)
    attraction_info = db_session.query(Attraction).filter_by(id=attraction_id).first()
    user = db_session.query(User).filter_by(username = session["user"]).first()
    user_achivements = db_session.query(Achievement).join(UserAchievement).filter(
        UserAchievement.user_id == user.id,
        Achievement.attraction_id == attraction_id
    ).all()

    print(user_achivements)

    if request.method == "POST" and passcode_form.validate():
        return redirect(url_for("unlock_achivement", attraction = attraction_id, passcode = passcode_form.passcode.data))

    return render_template("attraction_page.html", 
                           title=attraction_info.name, 
                           info=attraction_info, 
                           image=attraction_info.image, 
                           form=passcode_form, 
                           achievements=None if not user_achivements else user_achivements
                           )