from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from utils import db_session, User

class SignUpForm(Form):
    username = StringField("Username", [validators.data_required(), validators.Length(min=1, max=50, message= "Username length must be between 1 and 50 charecters.")])
    first_name = StringField("First name", [validators.data_required(), validators.Length(min=1, max=50, message= "First name required.")])
    last_name = StringField("Last name", [validators.data_required(), validators.Length(min=1, max=50, message= "Last name required.")])
    email = EmailField("E-mail address", [validators.data_required()])
    password = PasswordField("Password", [validators.data_required(), validators.equal_to("confirm", message="Passwords must match"), validators.Length(min = 8, max=255)])
    confirm = PasswordField("Confirm password")

    def validate_username(self, username):
        if db_session.query(User.id).filter_by(username=username.data).first() is not None:
            raise ValidationError("Username is already taken.")


    def validate_email(self, email):
        if db_session.query(User.id).filter_by(email=email.data).first() is not None:
            raise ValidationError("Email is already taken.")
