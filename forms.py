from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, StringField
from wtforms.validators import DataRequired, ValidationError
import datetime


def check_date_format(form, field):
    """ Validate date input format"""
    try:
        field.data = datetime.datetime.strptime(field.data, '%d/%m/%Y')
        field.data = field.data.strftime('%d/%m/%Y')
    except ValueError:
        raise ValidationError('Invalid date format.')


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = StringField('Date (dd/mm/yyyy)', validators=[DataRequired(), check_date_format])
    duration = IntegerField('Duration in minutes (integer only)', validators=[DataRequired()])
    learned = TextAreaField('Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources', validators=[DataRequired()])
