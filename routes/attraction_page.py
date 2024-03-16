from __main__ import app
from flask import render_template, request
from db_utils import db_session, Attraction, User, Achievement
from libs.helpers import require_login

@app.route('/attraction/<attraction_id>', methods=["GET"])
def view_attraction(attraction_id: int):
    attraction_info = db_session.query(Attraction).filter_by(id=attraction_id).first()

    return render_template("attraction_page.html", title=attraction_info.name, info=attraction_info, image=attraction_info.image)