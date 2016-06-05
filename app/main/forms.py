from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField,\
    TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from flask.ext.pagedown.fields import PageDown, PageDownField, TextAreaField


class EditProfileForm(Form):
    name = StringField('姓名', validators=[DataRequired()])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class PostForm(Form):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    pagedown = PageDownField("内容", validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(Form):
    email = StringField('你的邮箱(用于生成头像)', validators=[DataRequired(), Email()])
    comment = TextAreaField('你的评论', validators=[DataRequired()])
    submit = SubmitField('提交')
