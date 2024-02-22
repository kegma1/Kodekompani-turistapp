from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from utils import Session

class SignUpForm(Form):
    username = StringField("Username", [validators.data_required(), validators.Length(min=1, max=255)])
    email = EmailField("E-mail address", [validators.data_required()])
    password = PasswordField("Password", [validators.data_required(), validators.equal_to("confirm", message="Passwords must match"), validators.Length(min = 8, max=255)])
    confirm = PasswordField("Confirm password")

    def validate_username(self, username):
        pass

    def validate_email(self, email):
        pass # cant validate email without database