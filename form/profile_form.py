from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError
from utils import db_session, User


class ProfileForm(Form):
    pass