from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField

class NameCheck(Form):
    name = StringField('Name')
    submit = SubmitField('Check')
