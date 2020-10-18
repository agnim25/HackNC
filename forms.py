from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DecimalRangeField

class AuthForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    new = StringField('New?')
    submit = SubmitField('Submit')

class PredictForm(FlaskForm):
    text = StringField('Text')
    submit = SubmitField('Submit')

class ReturnForm(FlaskForm):
    submit = SubmitField('Submit')

