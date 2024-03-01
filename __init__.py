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
import routes.admin
import routes.profile

import routes.map_test

if __name__ == "__main__":
    app.run()

