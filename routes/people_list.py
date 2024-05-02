from __main__ import app
from db_utils import db_session, User
from flask import render_template, url_for, redirect
from libs.helpers import paging

@app.route("/people_list/<int:page>", methods=["GET"])
def people_list(page: int): 
    data = paging(page, 5, User, filter_deleted=True)
    
    if not data:
        return redirect(url_for("people_list", page = 1))

    return render_template("people_list.html", title="people", page=page, users = data)