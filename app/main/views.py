from . import main
from flask import request, render_template
from ..models import Post

#主索引页
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    print(type(posts))
    return '<h1>Hello world</h1>'



# 个人索引页
@main.route('/user/<name>')
def user_index(name):
    return "<h1>This is %s index!</h1>" % name


# 单个文章主页
@main.route('/post/<int:post_id>')
def post(post_id):
    return "<h1>This is the permanent of particular post %s</h1>" % post_id


# 用户编辑自己个人资料页面
@main.route('/edit-profile')
def edit_profile():
    pass


# 作者编辑自己的文章
@main.route('/edit-post/<int:post_id>')
def edit_post():
    pass

