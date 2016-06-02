from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField,\
    TextAreaField, ValidationError
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email, Regexp
from flask.ext.pagedown.fields import PageDown, PageDownField, TextAreaField


class EditProfileForm(Form):
    name = StringField('姓名', validators=[DataRequired()])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class PostForm(Form):
    pagedown = PageDownField("PageDownField", validators=[DataRequired()])
    submit = SubmitField('Submit')
