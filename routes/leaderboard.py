from __main__ import app
from flask import redirect, render_template, url_for, redirect, session
from db_utils import db_session, User
from libs.helpers import paging

@app.route("/leaderboard/<int:page>", methods = ["GET"]) 
def leaderboard(page):
    users = paging(page, 10, 
                   query=db_session.query(User).filter(User.isDeleted == False).order_by(User.xp_collected.desc()))
    
    if not users:
        return redirect(url_for("leaderboard", page = 1))
    
    return render_template("leaderboard.html",title="Leaderboard", users = users, page = page)