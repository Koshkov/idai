from flask_wtf import FlaskForm, CSRFProtect
from wtforms import TextAreaField, SubmitField, RadioField, StringField, BooleanField
from wtforms.validators import DataRequired, Length

class AICheckForm(FlaskForm):
    text = TextAreaField('',
                       validators=[DataRequired(),Length(10,8000)])
    submit = SubmitField('Detect')
