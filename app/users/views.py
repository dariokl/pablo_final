from .. import db
from ..models import User
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from . import users
from .forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, ResendVerification
from ..email import send_email


@users.route('/register', methods=['POST', 'GET'])
def register():
    """ Simple registration view , using flask_WTF and sending the email to the user with sendGrind in order to
    access they're accounts and proceed with the training scheduling"""

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, \
                    password=form.password.data, city=form.city.data, country=form.country.data,\
                    company=form.company.data, phone_number=form.phone.data, vat_tax_id=form.vat.data)
        db.session.add(user)
        db.session.commit()
        send_email(user.email, 'Confirm your Account !',
                    'email/register', user=user, token=user.generate_confirm_token())
        flash('You account is successfully created, please check your email and confirm your account')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    """Straight forward with this , simple form validation check and redirection to the index page , we use Flask-Login
    next query string argument, which can be accessed from the request.args dictionary.
    If the next query string argument is not available, a redirect to the home page is issued instead."""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # After querying over users to find the one with username from form we use verify_password method to check
        # if password was correct and then proceed to log user in .
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are logged in')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('core.index')
            return redirect(next)
        flash('Wrong username or password')

    return render_template('users/login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for(('core.index')))


@users.route('/confirm/<token>')
@login_required
def confirm(token):
    """ After the user recieve  the email up on clicking the link he will be redirected here note all that confirmation
    work is already done inside the user Model and we just commit the changes up inside the view if they pass the confirm
    method."""
    if current_user.confirmed:
        return redirect(url_for('core.index'))

    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account")
    else:
        flash("The confirmation link is invalid or has expired.")

    return redirect(url_for('core.index'))


@users.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user.email, 'Reset Your password!',
                       'email/reset_password', user=user, token=user.generate_password_reset_token())
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """  After the user clicks on the link in email we use @staticmethod from user model which reads the data in token
    data in token is the users id , i do the query over the model and return that user model and proceed to use
    set_password method to change the password """

    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('core.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('users.login'))
    return render_template('users/resetpassword.html', form=form)


@users.route('/verify_resend', methods=['GET', 'POST'])
def verify_resend():
    form = ResendVerification()

    if form.validate_on_submit():
        send_email(current_user.email, 'Confirm your Account !',
                   'email/register', user=current_user, token=current_user.generate_confirm_token())
        flash('Verification email has been sent, check your inbox for instructions !')

        return redirect(url_for('core.index'))

    return render_template('users/resend_verify.html', form=form)