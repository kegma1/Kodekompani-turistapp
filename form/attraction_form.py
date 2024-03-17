from wtforms import Form, StringField, IntegerField, validators, ValidationError, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AttractionForm(FlaskForm):
    name = StringField("Name", [validators.data_required()])
    description = StringField("Description", [validators.data_required()])
    category = StringField("Category", [validators.data_required()])
    age_recommendation = SelectField(choices=[0, 1, 3, 6, 9, 13, 18], validators=[validators.data_required()])
    location_coordinates = StringField("Location coordinates")
    address = StringField("address", [validators.data_required()])
    group = IntegerField("group")
    keywords = StringField("keywords", [validators.data_required()])

    image = FileField("Image banner", validators=[FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"], "Only images"), FileRequired()])
