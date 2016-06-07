from flask import jsonify, g, request

from .errors import forbidden
from .. import db
from . import api
from .authentication import auth
from ..models import Comment, Post


@api.route('/post/<int:id>/comments/', methods=['POST'])
@auth.login_required
def new_post_comments(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.post=post
    db.session.add()
    db.session.commit()
    return jsonify(comment.to_json())


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/comments/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.post.author:
        forbidden('no permission')
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'delete': True})


@api.route('/test', methods=['GET'])
@auth.login_required
def test():
    return jsonify({'areyoulogin': 'yes'})