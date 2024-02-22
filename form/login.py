from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from utils import Session

class LogInForm(Form):
    username = StringField("Username", [validators.data_required(), validators.Length(min=4, max=255)])
    password = PasswordField("Password", [validators.data_required(), validators.Length(min = 8, max=255)])