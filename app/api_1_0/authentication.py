from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import AnonymouseUserMixin

from ..exceptions import ValidationError
from ..models import User
from .errors import bad_request

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = AnonymouseUserMixin()
        return True
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
