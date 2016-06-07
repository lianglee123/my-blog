from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import AnonymousUserMixin

from ..exceptions import ValidationError
from ..models import User
from .errors import bad_request, unauthorized, forbidden
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = AnonymousUserMixin()
        return True
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    print('in auth_error: sorry, you password is wrong')
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Uniconfirmed account')
