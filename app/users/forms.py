from flask_wtf import FlaskForm
from flask import flash
import phonenumbers
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    """ Registration form that checks for valid username, email and password using the Regexps in order to keep password
    in desirable form , right now its set that username can only contain Letters and numbers it can be changed to more
    complex regex requirement if needed"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])


    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired(), \
                                                                EqualTo('pass_confirm', message='Password must match')])

    pass_confirm = PasswordField("Comfirm your password", validators=[DataRequired()])
    city = StringField('City name ', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    company = StringField('Company name')
    phone = StringField('Phone number', validators=[DataRequired()])
    vat = StringField(validators=[DataRequired()])

    submit = SubmitField("Register")

    # Used to check if the user email exists in the current database and returns ValidationEerror in that case
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('Email already registered')
            raise ValidationError('Email already registered')

    # Used to check if the users username exists in the current database and returns ValidationEerror in that case
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            flash('Username already taken')
            raise ValidationError('Username already taken')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            flash('Invalid phone number !')
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                                             EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ResendVerification(FlaskForm):
    submit = SubmitField('Resend Verification Email')
