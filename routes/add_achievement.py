from __main__ import app

from flask import redirect, render_template, url_for, request, flash
from db_utils import db_session, Achievement  # Make sure this is the correct import path
from form.achievement_form import AchievementForm  # Adjust to your actual form import path
from libs.helpers import require_local_admin, require_login
from werkzeug.datastructures import CombinedMultiDict

@app.route("/add_achievement", methods=["GET", "POST"])
@app.route("/add_achievement/<attraction_id>", methods=["GET", "POST"])
@require_login
@require_local_admin
def add_achievement(attraction_id = None):
    achievement_form = AchievementForm(data_required=True, formdata=CombinedMultiDict((request.files, request.form)))

    achievement_form.attraction_id.disabled = attraction_id is None
    if attraction_id:
        achievement_form.attraction_id.data = attraction_id

    if request.method == "POST" and achievement_form.validate_on_submit():
        new_achievement = Achievement()

        new_achievement.name = achievement_form.name.data
        new_achievement.description = achievement_form.description.data
        new_achievement.pass_code = achievement_form.pass_code.data
        new_achievement.xp_reward = achievement_form.xp_reward.data
        new_achievement.attraction_id = achievement_form.attraction_id.data
        new_achievement.age_rating = achievement_form.age_rating.data

        db_session.add(new_achievement)
        db_session.commit()

        flash("Achievement added successfully.", "success")
        return redirect(url_for("admin_achievements", page=1, attraction_id=attraction_id))
        
    return render_template("admin_add_achievement.html", title="Add Achievement", form=achievement_form, attraction_id=attraction_id)

