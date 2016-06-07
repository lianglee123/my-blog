from flask import jsonify, request, url_for, g, redirect

from .. import db
from . import api
from .errors import forbidden
from ..models import User, Post, Comment
from .authentication import auth


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for('api.get_posts', page=page-1, _external=True)
    _next = None
    if pagination.has_next:
        _next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': _next,
        'pages': pagination.pages,
        'count': pagination.total,
    })


@api.route('/post/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json)


@api.route('/post/<int:id>', methods=['PUT'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author != g.current_user:
        return forbidden('no permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


@api.route('/post/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != g.current_user:
        return forbidden('no permissions')
    db.session.delete(post)
    db.session.commit()
    return jsonify({'delete': True})


@api.route('/posts/', methods=['POST'])
@auth.login_required
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/post/<int:id>/comments/')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    page=request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(post_id=post.id).order_by(Comment.create_time.desc()).\
        paginate(page, 20, error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for('api.get_posts', page=page-1, _external=True)
    _next = None
    if pagination.has_next:
        _next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in comments],
        'prev': prev,
        'next': _next,
        'pages': pagination.pages,
        'count': pagination.total,
    })



