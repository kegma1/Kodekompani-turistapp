from wtforms import StringField, IntegerField, validators, SelectField, TextAreaField, HiddenField
from flask_wtf import FlaskForm

class AchievementForm(FlaskForm):
    def __init__(self, data_required, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)
        if data_required:
            self.name.validators = [validators.data_required()]
            self.description.validators = [validators.data_required()]
            self.pass_code.validators = [validators.data_required()]
            self.xp_reward.validators = [validators.data_required(), validators.number_range(min=0)]
            self.attraction_id.validators = [validators.data_required(), validators.number_range(min=1)]
            self.age_rating.validators = [validators.optional(), validators.number_range(min=0)]

    name = StringField("Name", validators=[validators.length(max=100)])
    description = TextAreaField("Description", validators=[validators.length(max=255)])
    pass_code = StringField("Pass Code", validators=[validators.length(max=255)])
    xp_reward = IntegerField("XP Reward", validators=[validators.number_range(min=0)])
    attraction_id = IntegerField("Attraction ID", validators=[validators.number_range(min=1)])
    age_rating = SelectField("Age Rating", choices=[('0', 'All Ages'), ('3', '3+'), ('6', '6+'), ('9', '9+'), ('12', '12+'), ('16', '16+'), ('18', '18+')], coerce=int, validate_choice=False)
