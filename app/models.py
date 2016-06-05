from . import db
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from .import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.Text(200))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    links = db.relationship('Link', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(),
                     password='liliang',
                     confirmed=True,
                     about_me=forgery_py.lorem_ipsum.sentence(),
                    )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False, default="默认标题")
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        from sqlalchemy.exc import IntegrityError
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(author_id=u.id,
                     body=forgery_py.lorem_ipsum.sentences(randint(50, 150)),
                     )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_title(default_title):
        from sqlalchemy.exc import IntegrityError
        for post in Post.query.all():
            if post.title is None:
                post.title = default_title
            db.session.add(post)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    author_email = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text, nullable=False)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        from sqlalchemy.exc import IntegrityError
        import forgery_py

        seed()
        post_count = Post.query.count()
        for i in range(count):
            p = Post.query.offset(randint(0, post_count-1)).first()
            c = Comment(post_id=p.id,
                        author_email = forgery_py.internet.email_address(),
                        body = forgery_py.lorem_ipsum.sentences(10),)
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    link_url = db.Column(db.String(200), nullable=False)
    link_name = db.Column(db.String(50))
    link_description = db.Column(db.String(100), nullable=False)

    @staticmethod
    def generate_fake(count=10):
        from random import randint, seed
        import forgery_py
        from sqlalchemy.exc import IntegrityError

        seed()
        user_count = User.query.count()
        for i in range(user_count):
            u = User.query.offset(i).first()
            for i in range(count):
                li = Link(user_id = u.id,
                         link_url = forgery_py.internet.domain_name(),
                         link_name = forgery_py.lorem_ipsum.words(3),
                         link_description = forgery_py.lorem_ipsum.sentences(4))
                db.session.add(li)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
