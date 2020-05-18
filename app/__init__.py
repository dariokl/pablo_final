from config import config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_mail import Mail

login_manager = LoginManager()
db = SQLAlchemy()
admin = Admin()
mail = Mail()


def create_app(confing_name):
    app = Flask(__name__)
    app.config.from_object(config[confing_name])
    config[confing_name].init_app(app)
    db.init_app(app)


    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint, url_prefix='/')

    from .admin.views import ExcludeModelView, AddSearchView
    from .models import Course, Teacher, User, Booking, CourseTeachers

    admin = Admin(app, url='/panel')
    admin.add_view(ExcludeModelView(Course, db.session))
    admin.add_view(AddSearchView(Teacher, db.session))
    admin.add_view(AddSearchView(User, db.session))
    admin.add_view(ExcludeModelView(CourseTeachers, db.session))
    admin.add_view(ExcludeModelView(Booking, db.session))

    return app