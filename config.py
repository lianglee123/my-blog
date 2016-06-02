import os


basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopConfig(Config):
    DEBUG = True
    SECRET_KEY = 'hard to guess string is it'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


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