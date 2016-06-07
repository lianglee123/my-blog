from flask import jsonify, request, url_for

from . import api
from ..models import User, Post


@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get_or_404()
    return jsonify(user.to_json)


@api.route('/user/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(author_id=id).paginate(
        page, 20, error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for('api.get_user_posts', id=id, page=page-1, _external=True)
    _next = None
    if pagination.has_next:
        _next = url_for('api.get_user_posts', id=id, page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': _next,
        'pages': pagination.pages,
        'count': pagination.total,
    })
