from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField("Please choose 1 name for yourself\n You can use your name",validators=[DataRequired()])
    submit = SubmitField(validators=[DataRequired()])