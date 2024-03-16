from wtforms import Form, StringField, IntegerField, validators, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AddAttraction(FlaskForm):
    name = StringField("Name", [validators.data_required()])
    description = StringField("Description", [validators.data_required()])
    category = StringField("Category", [validators.data_required()])
    age_recommendation = IntegerField("Age recommendation", [validators.data_required()])
    location_coordinates = StringField("Location coordinates")
    address = StringField("address", [validators.data_required()])
    group = IntegerField("group")
    keywords = StringField("keywords")

    image = FileField("Image banner", validators=[FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"], "Only images"), FileRequired()])
