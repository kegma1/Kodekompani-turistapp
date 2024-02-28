from wtforms import Form, StringField, PasswordField, validators, ValidationError
from libs.db_utils import db_session, User
from werkzeug.security import check_password_hash

class LogInForm(Form):
    pass_min = 8
    pass_max = 255
    username = StringField("Username", [validators.data_required(), validators.Length(min=1, max=255)])
    password = PasswordField("Password", [validators.data_required(), validators.Length(min = pass_min, max= pass_max, message=f"Password requires length of {pass_min} to {pass_max}.")])
    
    def validate_username(self, username):
        if db_session.query(User.id).filter_by(username = username.data).first() == None:
            raise ValidationError("Username does not exist.")
        
    def validate_password(self, password):
        user_password = db_session.query(User.encrypted_password).filter_by(username= self.username.data).first()
        if user_password is not None and not check_password_hash(user_password[0], password.data):
            raise ValidationError("Password is not correct.")  
        