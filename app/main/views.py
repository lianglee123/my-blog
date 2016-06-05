from . import main
from flask import request, jsonify, flash, abort, render_template,\
    redirect, url_for, session
from flask.ext.login import login_required, current_user
from ..models import Post, User, Comment
from .forms import EditProfileForm, PostForm, CommentForm
from .. import db
from flask.ext.login import login_required


# 主索引页
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


# 个人索引页
@main.route('/user/<name>')
def user_index(name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = name).first()
    pagination = Post.query.filter_by(author_id=user.id).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts)


# 单个文章主页
@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    page = request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post=post,
                          author_email=form.email.data,
                          body=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash('你的评论已提交')
        pagination = Comment.query.filter_by(post_id=post.id).paginate(
            page, per_page=20, error_out=False)
        return redirect(url_for('.post', post_id=post.id, page=pagination.pages))
    else:
        pagination = Comment.query.filter_by(post_id=post.id).paginate(
            page, per_page=20, error_out=False)
        comments = pagination.items
        return render_template('main/post.html',posts=[post], pagination=pagination,
                           comments=comments, form=form)


# 用户编辑自己个人资料页面
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('You profile has been updated.')
        return redirect(url_for('main.edit_profile'))
    form.name.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


# 作者编辑自己的文章
@main.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.pagedown.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', post_id=post.id))
    post = Post.query.get_or_404(post_id)
    form.title.data = post.title
    form.pagedown.data = post.body
    return render_template('main/write_post.html', form=form)


@main.route('/write', methods=['GET', 'POST'])
@login_required
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(author=current_user,
                    title=form.title.data,
                    body=form.pagedown.data)
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        print(type(post.id))
        return redirect(url_for('.post', post_id=post.id))
    form.title.data = '请输入标题'
    form.pagedown.data = '在此处编辑文章'
    return render_template('main/write_post.html', form=form)


# 删除评论
@main.route('/dele-comment/<int:id>')
@login_required
def dele_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user.id != comment.post.author_id:
        abort(403)
    db.session.delete(comment)
    print(request.args)
    pre_url = request.args.get('pre_url')
    return redirect(pre_url)

@main.route('/test')
def test():
    print(request.args)
    return render_template('test.html')