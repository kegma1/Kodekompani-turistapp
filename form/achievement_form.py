from wtforms import StringField, IntegerField, validators, SelectField, TextAreaField, BooleanField
from flask_wtf import FlaskForm
from db_utils import db_session, Attraction

class AchievementForm(FlaskForm):
    def __init__(self, data_required, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)

        attraction_list = [(attraction.id, attraction.name) for attraction in db_session.query(Attraction).all()]

        self.attraction_id.choices = attraction_list

        if data_required:
            self.name.validators = [validators.DataRequired()]
            self.description.validators = [validators.DataRequired()]
            self.pass_code.validators = [validators.DataRequired()]
            self.xp_reward.validators = [validators.DataRequired(), validators.NumberRange(min=0)]
            self.attraction_id.validators = [validators.DataRequired()]
            self.age_rating.validators = [validators.Optional(), validators.NumberRange(min=0)]
            self.is_deleted.default = False

    name = StringField("Name", validators=[validators.Length(max=100)])
    description = TextAreaField("Description", validators=[validators.Length(max=255)])
    pass_code = StringField("Pass Code", validators=[validators.Length(max=255)])
    xp_reward = IntegerField("XP Reward", validators=[validators.NumberRange(min=0)])
    # attraction_id = IntegerField("Attraction ID", validators=[validators.NumberRange(min=1)])
    
   
    attraction_id = SelectField("Attraction", coerce=int, validate_choice=False)
    age_rating = SelectField("Age Rating", choices=[('0', 'All Ages'), ('3', '3+'), ('6', '6+'), ('9', '9+'), ('12', '12+'), ('16', '16+'), ('18', '18+')], coerce=int, validate_choice=False)
    is_deleted = BooleanField("Is Deleted")