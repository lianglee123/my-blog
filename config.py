import os


basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class DevelopConfig(Config):
    DEBUG = True
    SECRET_KEY = 'hard to guess string is it'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SENDER = 'Flasky Admin <18737455730@163.com>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    FLASKY_MAIL_SUBJECT_PREFIX = '[My Blog]'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

config = {
    'develop': DevelopConfig,
    'default': DevelopConfig,
    'testing': TestConfig,
}