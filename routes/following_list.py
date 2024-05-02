from __main__ import app
from flask import render_template, redirect, url_for
from db_utils import db_session, User

@app.route('/followers_list/<id>/<int:page>', methods=["GET"])
def followers_list(id, page):
    url_name = 'followers_list'
    
    user = db_session.query(User).filter_by(id = id).first()
    
    followers = [user for user in user.followers if not user.isDeleted][(page*5)-5 : (page*5)] #Crude ahh paging pga relationship mellom Friend table og User table
    
    if not followers and page != 1:
        return redirect(url_for(url_name, id = id, page = 1))

    return render_template("follow_list.html", userlist = followers, prev_user = user, url_name = url_name, id = id, page = page)

@app.route('/following_list/<id>/<int:page>', methods=["GET"])
def following_list(id, page):
    url_name = 'following_list'
    user = db_session.query(User).filter_by(id = id).first()
    
    following = [user for user in user.following if not user.isDeleted][(page*5)-5 : (page*5)] #Crude ahh paging pga relationship mellom Friend table og User table
    
    if not following and page != 1:
        return redirect(url_for(url_name, id = id, page = 1))

    return render_template("follow_list.html", userlist = following, prev_user = user, url_name = url_name, id = id, page = page)