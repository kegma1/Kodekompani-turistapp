from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from utils import Session

class LogInForm(Form):
    pass_min = 8
    pass_max = 255
    username = StringField("Username", [validators.data_required(), validators.Length(min=1, max=255)])
    password = PasswordField("Password", [validators.data_required(), validators.Length(min = pass_min, max= pass_max, message=f"Password requires length of {pass_min} to {pass_max}.")])
    