from flask import Flask, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import date
from db_utils import db_session, User
app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

import routes.index
import routes.signup
import routes.login
import routes.logout
import routes.admin
import routes.admin_sights
import routes.profile
import routes.attractions_list
import routes.attraction_page
import routes.map_test

if __name__ == "__main__":
    app.run()

# user1 = user1pass
# user2 = user2pass
# admin1 = admin1pass