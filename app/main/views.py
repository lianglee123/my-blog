from . import main
from flask import request, jsonify, flash, abort, render_template,\
    redirect, url_for
from flask.ext.login import login_required, current_user
from ..models import Post, User
from .forms import EditProfileForm, PostForm
from .. import db
from flask.ext.login import login_required


#主索引页
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    print(type(posts))
    return jsonify({'post': str(posts), 'pagination': str(pagination)})


# 个人索引页
@main.route('/user/<name>')
def user_index(name):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(title=name).order_by(Post.create_time.desc).paginate(
        page, per_page=20, error_out=True)
    posts = pagination.items
    return jsonify({'posts': str(post), 'pagination': str(pagination)})


# 单个文章主页
@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'post': str(post)})


# 用户编辑自己个人资料页面
@main.route('/edit-profile')
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('You profile has been updated.')
        return jsonify({'redirect': 'url_for(main.user)个人索引页'})
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    return jsonify({'template':'edit_profile.html',
                    'form': str(form)})


# 作者编辑自己的文章
@main.route('/edit-post/<int:post_id>')
# @login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    # if current_user != post.author:
    #     abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    post = Post.query.get_or_404(post_id)
    form.pagedown.data = post.body
    return render_template('main/pagedown_test.html', form=form)


