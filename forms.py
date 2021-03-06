from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField("Please choose 1 name for yourself\n You can use your name",validators=[DataRequired()])
    submit = SubmitField(validators=[DataRequired()])


class ThoughtForm(FlaskForm):
    topic = StringField("Topic (One word)", validators=[DataRequired()])
    thought = TextAreaField("Record Your thoughts", validators=[DataRequired()])
    submit = SubmitField(validators=[DataRequired()])