import os
from dotenv import load_dotenv

load_dotenv()

#used to create SQLite db for development
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """ The main config class required setup in .env type of file make sure you delete all the or statements
    adding send grind would be the best option to handle the daily email flow"""
    #Mail setup
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    USE_MAIL_TLS = os.environ.get('USE_MAIL_TLS' or 'True')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # This is 'apikey' from sendgrid
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # the api key from send grid
    MAIL_SENDER = os.environ.get('MAIL_SENDER') # send grid email
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    APP_ADMIN = os.environ.get("APP_ADMIN") # THIS IS THE ADMINS EMAIL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://{user}:{pw}@{url}/{db}'.format(user=os.environ.get('MYSQL_USER'),\
                                                                                    pw=os.environ.get('MYSQL_PW'),\
                                                                                    url=os.environ.get('MYSQL_URL'),\
                                                                                    db=os.environ.get('MYSQL_DB'))


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-database.sqlite')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
