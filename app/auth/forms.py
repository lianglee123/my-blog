from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    username = SubmitField('用户名', validators=[
        DataRequired(), Length(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                         'Username must have only letters,'
                                         'number, dots or underscores.')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')



class ChangePassword(Form):
    old_password = StringField('原密码', validators=[DataRequired(), Length(1, 64)])
    new_password = StringField('新密码', validators=[
        DataRequired(), EqualTo('new_password2', message='Password must match')])
    new_password2 = StringField('密码确认', validators=[DataRequired()])
    submit = SubmitField('确认')