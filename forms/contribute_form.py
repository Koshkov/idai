from flask_wtf import FlaskForm, CSRFProtect
from wtforms import TextAreaField, SubmitField, RadioField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class ContributeForm(FlaskForm):
    ai_status = SelectField('Source:',  choices=[('ai', 'AI Generated'), ('human', 'Human')], validators=[DataRequired()])
    text = TextAreaField('',validators=[DataRequired(),Length(10,8000)])
    permission = BooleanField('I have permisson to share this work.',validators=[DataRequired()])
    submit = SubmitField('Contribute')

