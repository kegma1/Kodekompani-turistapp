from wtforms import Form, StringField, PasswordField, EmailField, validators, ValidationError, DateField
from utils import db_session, User
from werkzeug.security import check_password_hash
from datetime import date, timedelta
from __main__ import session


class ProfileForm(Form):
    username = StringField("Username:", [validators.data_required(), validators.Length(min=1, max=50, message= "Username length must be between 1 and 50 charecters.")])
    first_name = StringField("First name:", [validators.data_required(), validators.Length(min=1, max=50, message= "First name required.")])
    last_name = StringField("Last name:", [validators.data_required(), validators.Length(min=1, max=50, message= "Last name required.")])
    year = DateField("Year o' birth:", [validators.data_required()])
    email = EmailField("Email address:", [validators.data_required()])
    password = PasswordField("Password:", [validators.data_required(), validators.equal_to("confirm", message="Passwords must match"), validators.Length(min = 8, max=255)])
    confirm = PasswordField("Confirm password:")

    def validate_username(self, username):
        if username == session['user']:
            raise ValidationError("Can't change to the previous username")
        if db_session.query(User.id).filter_by(username=username.data).first() is not None:
            raise ValidationError("Username is already taken.")
    
    def validate_year(self, year):
        if year.data > date.today():
            raise ValidationError("You cannot be younger than today.")
        
        if year.data < (date.today() - timedelta(days= 123 * 365.25)):
            raise ValidationError("Cannot be older than 123 years old.")