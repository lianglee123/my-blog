# my-blog
A personal blog powered by Flask.

### main:
主索引页 ('/', index(), 'indext.html')

个人索引页 ('/user/<username>', user(username), 'user.html')

单个文章页 ('/post/<int: id>', post(id), 'post.html')

用户编辑自己个人资料页 ('/edit-profile', edit_profile(), 'edit_profile.html')

作者编辑自己文章页 ('/edit-profile/<int: user_id>', edit_profile_admin(id),  'main.user' or 'edit_profile.html')

写文章页 ('/editpost/<int: post_id>',  edit(id), 'main.post' or 'edit_post.html')

### auth:

注册 ('/register', register(),  'auth.login' or 'auth/register.html'）

登录 ('/login',   login(),  'next' or 'main.index' or 'auth/login.html'

登出 ('/logout', logout(), 'main.index')

账户确认 ('/confirm',  resend_confirmation(),  'main.index')
('/confirm/<token>',  confirm(), 'main.index')
('/unconfirmed'， unconfirmed(),    'main.index' or 'auth/unconfirmed.html')

修改密码 ('/change-password',   change_password(),  'auth/change_passwoed.html' or 'main.index')

重置密码 ('/reset',   password_reset_request()， 'auth/reset_password.html' or 'auth.login')
('/reset/<token>', password_reset(), 'auth/reset_password.html' or 'auth.login' or 'main.index'

修改邮箱 ('/change-email', change_email_request(), 'auth/change_email.html' or 'main.index')
('/change-email/<token>', change_email(), 'main.index')

![image1](http://p1.bqimg.com/1949/dcd1db29fd420a98.png)
