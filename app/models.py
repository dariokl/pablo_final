from flask import current_app
from app import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64),nullable=False)
    city = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64))
    password_hash= db.Column(db.String(128))
    vat_tax_id = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    orders = db.relationship('Booking', backref='customer_info', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None:
            if self.email == current_app.config['APP_ADMIN']:
                self.is_admin = True
            else:
                self.is_admin = False


    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    # Generating password with werkzeug.secuirty generate_password_hash method.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Simple password check with werkzeug.security check_password_hash method.
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    #Generate the Json and dump it with Serializer
    def generate_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    #Generate the password reset token
    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            id = data.get('confirm')
        except:
            return
        return User.query.get(id)


    #Reading the token with Serializer
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            False

        #If the token is not validated it will return False
        if data.get('confirm') != self.id:
            return False

        #If the validation is successfull we change the self.confirmed property to True
        self.confirmed = True
        db.session.add(self)
        return True

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)



class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    dni = db.Column(db.String(64), unique=True, nullable=False)

    assigned_date = db.relationship('Booking', backref='teacher_info', lazy='dynamic')
    teacher_name = db.relationship('CourseTeachers', backref='teacher', lazy='dynamic')


    def __init__(self, **kwargs):
        super(Teacher, self).__init__(**kwargs)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)



class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    course_info = db.relationship('Booking', backref='training_info', lazy='dynamic')
    course_name = db.relationship('CourseTeachers', backref='training_type', lazy='dynamic')


    def __init__(self, **kwargs):
        super(Course, self).__init__(**kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Booking(db.Model):

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    def __init__(self, **kwargs):
        super(Booking, self).__init__(**kwargs)


class CourseTeachers(db.Model):

    __tablename__ = 'coursesteachers'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), primary_key=True)

    def __init__(self, **kwargs):
        super(CourseTeachers, self).__init__(**kwargs)




class AnonymousUser(AnonymousUserMixin):
    def admin_level(self):
        return 'AnonUser'

    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser