from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from werkzeug.security import check_password_hash

class SignUpForm(Form):
    username = StringField("Username", [validators.data_required(), validators.Length(min=4, max=255)])
    email = EmailField("E-mail address", [validators.data_required()])
    password = PasswordField("Password", [validators.data_required(), validators.equal_to("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm password")

    def validate_username(self, username):
        pass # cant validate username without database

    def validate_email(self, email):
        pass # cant validate email without database