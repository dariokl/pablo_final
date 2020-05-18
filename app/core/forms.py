from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, DateField, TextAreaField
from wtforms.validators import Email, DataRequired


class BookingForm(FlaskForm):
    """Booking form used as hidden field to send the value of the training.id after the form submits"""
    name = StringField('Select This Course')
    date = DateField('Date', format='%d/%m/%Y')
    submit = SubmitField('Enter')


class ContactUsForm(FlaskForm):

    email = StringField('Your email', validators=[DataRequired(), Email()])
    text  = TextAreaField('Write...', validators=[DataRequired()])
    name  = StringField()
    company = StringField()
    submit = SubmitField('Send Mail')
