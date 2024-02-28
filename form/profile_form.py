from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError, DateField
from libs.db_utils import db_session, User
from werkzeug.security import check_password_hash
from datetime import date, timedelta
from __main__ import session


class ProfileForm(Form):
    username = StringField("Username:", [validators.data_required(), validators.Length(min=1, max=50, message= "Username length must be between 1 and 50 charecters.")])
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    year = DateField("Year o' birth:")
    email = EmailField("Email address:", [validators.data_required()])
    old_password = PasswordField("Old Password:")
    password = PasswordField("Password:")
    confirm = PasswordField("Confirm password:")

    def validate_username(self, username):
        if username == session['user']:
            raise ValidationError("Can't change to the previous username")
        if db_session.query(User.id).filter_by(username=username.data).first() is not None:
            raise ValidationError("Username is already taken.")