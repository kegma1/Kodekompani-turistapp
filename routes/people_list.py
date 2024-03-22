from __main__ import app
from db_utils import db_session, User
from flask import render_template, url_for, redirect

@app.route("/people_list/<page>", methods=["GET"])
def people_list(page: int):
    page = int(page)
    if page < 1:
        return redirect(url_for("people_list", page = 1)) 

    users = db_session.query(User).offset((page * 5) - 5).limit(5).all()

    if not users and page != 1:
        return redirect(url_for("people_list", page = 1)) 

    return render_template("people_list.html", title="people", page=page, users=users)