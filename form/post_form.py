from wtforms import TextAreaField, SelectField, HiddenField, validators
from flask_wtf import FlaskForm
from db_utils import db_session, Attraction

class PostForm(FlaskForm):
    def __init__(self, attraction = None, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)

        if attraction:
            (name,) = db_session.query(Attraction.name).filter_by(id = attraction).first()
            self.attraction.choices = [(attraction, name)]
        else:
            attraction_list = [( 0, "No attraction selected")] + [(attraction.id, attraction.name) for attraction in db_session.query(Attraction).all()]

            self.attraction.choices = attraction_list
        
    message = TextAreaField("Message", validators=[validators.data_required()])
    attraction = SelectField("Attraction", validate_choice=False, coerce=int)