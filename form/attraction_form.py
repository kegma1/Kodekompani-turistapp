from wtforms import StringField, IntegerField, validators, SelectField, TextAreaField, BooleanField, HiddenField, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from db_utils import db_session, User
from libs.helpers import is_admin
from flask import session


class AttractionForm(FlaskForm):
    def __init__(self, data_required, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)
        self.location_coordinates.validators = [validators.Regexp(r'^-?\d+.\d+,\s*-?\d+.\d+$', message="invalid coordinates format.")]
        
        self.local_admin.choices = [(attraction.id, attraction.username) for attraction in db_session.query(User).all()]

        if data_required:
            self.image.validators = [FileRequired(), FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"], "Only images")]
            self.name.validators = [validators.data_required()]
            self.description.validators = [validators.data_required()]
            self.category.validators = [validators.data_required()]
            self.age_recommendation.validators = [validators.data_required()]
            self.address.validators = [validators.data_required()]
            self.location_coordinates.validators = [validators.data_required(), validators.Regexp(r'^-?\d+.\d+,\s*-?\d+.\d+$', message="invalid coordinates format.")]
            self.local_admin.validators = [validators.data_required()]

    name = StringField("Name")
    description = TextAreaField("Description")
    category = StringField("Category")
    age_recommendation = SelectField(choices=[0, 1, 3, 6, 9, 13, 18], validate_choice=False)
    location_coordinates = HiddenField("Location coordinates", default="68.430,17.200")
    address = StringField("address")
    isDeleted = BooleanField(default=False, label="Delete?")

    image = FileField("Image banner", validators= [FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"], "Only images")])

    local_admin = SelectField("Local admin", validate_choice=False, coerce=int)



