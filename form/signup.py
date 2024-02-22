from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from utils import Session, User

class SignUpForm(Form):
    username = StringField("Username", [validators.data_required(), validators.Length(min=4, max=255)])
    email = EmailField("E-mail address", [validators.data_required()])
    password = PasswordField("Password", [validators.data_required(), validators.equal_to("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm password")

    def validate_username(self, username):
        if Session.query(User.id).filter_by(username=username.data).first() is not None:
            raise ValidationError("Username is allready taken.")


    def validate_email(self, email):
        if Session.query(User.id).filter_by(email=email.data).first() is not None:
            raise ValidationError("Username is allready taken.")
