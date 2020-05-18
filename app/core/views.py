from .. import db
from ..email import send_email
from ..models import Teacher, Course, Booking, CourseTeachers
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from . import core
from .forms import BookingForm, ContactUsForm
from dateutil import parser



@core.route('/')
def index():
    return render_template('index.html')


@core.route('/booking', methods=['POST', 'GET'])
@login_required
def booking():
    """ The most complex view and the core of application , i will try to details all the steps ,
    first after a user submits a form , which contains date ( d/mm/yyyy) the date is sent back and parsed to be imported
    in date column of database , same happens to the course which contains the hidden value form that is PK of the
    Course.id ( this can be found in the BookingForm , on booking.html ), after that i do one query that filters
    teachers_ids inside the Booking model , it returns all the booked teachers on that date, in the second query all the
    free teachers are listed we note that we use NOTIN_ operator from SQLAlchemy so we search for the teachers.id that are
    not booked on that day. We now have a query that contains teachers that are not assigned to any of the courses , now
    we proceed to find the teachers based on picked 'course type' (docker.etc) then we use IN_ operator which of one of
    free teachers is linked to the selected course."""

    coruses_list = Course.query.all()
    form = BookingForm()

    if form.validate_on_submit():
        date = request.form.get('date')
        date_obg = parser.parse(date)
        course = request.form.get('name')

        # Main teachers queries , taken_teacher is base query of all taken teachers_on picked date and type of course.
        taken_teachers = db.session.query(Booking.teacher_id).filter(Booking.start == date_obg)

        free_teachers = db.session.query(Teacher.id).filter(Teacher.id.notin_(taken_teachers))

        course_type_teacher = [q[0] for q in db.session.query(CourseTeachers.teacher_id)\
            .filter(CourseTeachers.course_id == course).filter(CourseTeachers.teacher_id.in_(free_teachers)).all()]


       #This could need future changes adding an enroll table would be helpful and application would scale better
        booked_user = db.session.query(Booking.user_id).filter(Booking.start == date_obg).all()
        print(booked_user)
        for id in booked_user:
            if current_user.id == id[0]:
                flash (" You are already booked in this week ! ")
                return redirect(url_for('core.index'))

        #Using try and except just in case there is no available teachers it will flash "Sorry we are Booked"
        try:
            teacher_to_mail = db.session.query(Teacher).filter(Teacher.id == course_type_teacher[0]).first()
            new = Booking(start=date_obg, user_id=current_user.id, course_id=course,
                      teacher_id=course_type_teacher[0])
            db.session.add(new)
            db.session.commit()
            flash (" You have successfully booked your training !")
            send_email(teacher_to_mail.email, 'New Class Appointment!',
                       'email/notify_teacher', teacher=teacher_to_mail, date=date_obg)
            send_email(current_user.email, 'Booking confirmation', 'email/notify_user', user=current_user,\
                        date=date_obg)
            return redirect(url_for('core.index'))
        except IndexError:
            flash ('Sorry we are Booked')
            return redirect(url_for('core.booking'))

    return render_template('booking.html', training_list=coruses_list, form=form)



@core.route('/architecture')
def architecture():

    return render_template('architecture.html')

@core.route('/implementation')
def implementation():

    return render_template('implementation.html')


@core.route('/courses')
def courses():
    all_trainings = Course.query.all()

    return render_template('training.html', all_trainings=all_trainings)

@core.route('contact_us', methods=["GET", "POST"])
def contact_us():

    form = ContactUsForm()

    if form.validate_on_submit():
        app = current_app._get_current_object()
        send_email(app.config['APP_ADMIN'], 'You have New Email', 'email/admin_contact', sender=form.email.data,\
                   text=form.text.data, name=form.name.data, company=form.company.data)
        flash('We received your email')
        return redirect(url_for('core.index'))

    return render_template('contact_us.html', form=form)

@core.route('/services')
def services():

    return render_template('services.html')

@core.route('/strategy')
def strategy():
    return render_template('strategy.html')

@core.route('/feedback')
def feedback():
    return render_template('feedback.html')