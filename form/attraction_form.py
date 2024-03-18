from wtforms import StringField, IntegerField, validators, SelectField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AttractionForm(FlaskForm):
    def __init__(self, data_required, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)
        self.location_coordinates.validators = [validators.Regexp(r'^\d+\.\d+,\s?\d+\.\d+$', message="invalid coordinates format.")]
        if data_required:
            self.image.validators = [FileRequired(), FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"], "Only images")]
            self.name.validators = [validators.data_required()]
            self.description.validators = [validators.data_required()]
            self.category.validators = [validators.data_required()]
            self.age_recommendation.validators = [validators.data_required()]
            self.address.validators = [validators.data_required()]
            self.keywords.validators = [validators.data_required()]
            self.location_coordinates.validators = [validators.data_required(), validators.Regexp(r'^\d+\.\d+,\s?\d+\.\d+$', message="invalid coordinates format.")]
    name = StringField("Name")
    description = TextAreaField("Description")
    category = StringField("Category")
    age_recommendation = SelectField(choices=[0, 1, 3, 6, 9, 13, 18], validate_choice=False)
    location_coordinates = StringField("Location coordinates")
    address = StringField("address")
    group = IntegerField("group")
    keywords = StringField("keywords")

    image = FileField("Image banner", validators= [FileAllowed(["png", "jpg", "jpeg", "jfif", "webp"], "Only images")])



