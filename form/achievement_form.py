from wtforms import StringField, IntegerField, validators, SelectField, TextAreaField, BooleanField
from flask_wtf import FlaskForm

class AchievementForm(FlaskForm):
    def __init__(self, data_required, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)
        if data_required:
            self.name.validators = [validators.DataRequired()]
            self.description.validators = [validators.DataRequired()]
            self.pass_code.validators = [validators.DataRequired()]
            self.xp_reward.validators = [validators.DataRequired(), validators.NumberRange(min=0)]
            self.attraction_id.validators = [validators.DataRequired(), validators.NumberRange(min=1)]
            self.age_rating.validators = [validators.Optional(), validators.NumberRange(min=0)]
            self.is_deleted.default = False

    name = StringField("Name", validators=[validators.Length(max=100)])
    description = TextAreaField("Description", validators=[validators.Length(max=255)])
    pass_code = StringField("Pass Code", validators=[validators.Length(max=255)])
    xp_reward = IntegerField("XP Reward", validators=[validators.NumberRange(min=0)])
    attraction_id = IntegerField("Attraction ID", validators=[validators.NumberRange(min=1)])
    age_rating = SelectField("Age Rating", choices=[('0', 'All Ages'), ('3', '3+'), ('6', '6+'), ('9', '9+'), ('12', '12+'), ('16', '16+'), ('18', '18+')], coerce=int, validate_choice=False)
    is_deleted = BooleanField("Is Deleted")