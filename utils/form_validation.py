from pyexpat.errors import messages

from flask_wtf import FlaskForm
from wtforms.validators import Regexp, Length, DataRequired, NumberRange
from wtforms import StringField, FloatField

string_length = Length(1, 10, "Text needs to be between 1 and 10 characters long")
regex = Regexp('[a-zA-Z]', message="Only English letters allowed")
required = DataRequired(message="All fields must be filled in")
seconds_range = NumberRange(0.5, 10.0, "Length must be between 0.5 and 10 seconds")

class SoundForm(FlaskForm):
    text = StringField('text', validators=[required, string_length, regex])
    slider = FloatField('slider', validators=[required, seconds_range])
