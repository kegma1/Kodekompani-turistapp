from wtforms import StringField, PasswordField, EmailField, validators, ValidationError, DateField, TextAreaField, BooleanField
from db_utils import db_session, User
from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class ProfileForm(FlaskForm):
    username = StringField("Username:", [validators.data_required(), validators.Length(min=3, max=50, message= "Username length must be between 3 and 50 charecters.")])
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    year = DateField("Year o' birth:")
    email = EmailField("Email address:", [validators.data_required()])
    old_password = PasswordField("Old Password:")
    password = PasswordField("Password:", [validators.equal_to("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm password:")
    bio = TextAreaField("Description:", [validators.length(min = 0, max= 255)])
    picture = FileField("Profile Picture:", [FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"])])
    keep_picture = BooleanField("Reset profile picture")

    def validate_username(self, username):
        if username.data == session['user']:
            pass
        elif db_session.query(User.id).filter_by(username=username.data).first() is not None:
            raise ValidationError("Username is already taken.")