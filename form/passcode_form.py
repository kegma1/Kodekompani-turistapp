from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError
from db_utils import db_session, Achievement, Attraction

class Passcode(FlaskForm):
    passcode = StringField("Enter passcode", [validators.data_required()])

    def __init__(self, attraction = None, formdata=..., **kwargs):
        super().__init__(formdata, **kwargs)
        self.attraction = attraction
    
    def validate_passcode(self, passcode):
        achivement = db_session.query(Achievement).join(Attraction).filter(Attraction.id==self.attraction, Achievement.pass_code==passcode.data).first()

        if not achivement:
            raise ValidationError("No achivements found with this passcode for this attraction.")
        if achivement.is_deleted:
            raise ValidationError("This achivement is disabled")
        

