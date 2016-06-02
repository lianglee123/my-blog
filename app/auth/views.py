from . import auth
from .forms import LoginForm, RegisterForm, ChangePassword
from ..models import User, Post
from flask.ext.login import login_user, logout_user, current_user,\
    login_required
from flask import redirect, request, url_for, flash, jsonify,\
    render_template
from ..email import send_email
from .. import db

@auth.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next')) or url_for('main.index')
        flash('Invalid username or password.')
    return jsonify({'template': 'auth/login.html', 'form':str(form)})


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A New confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation links is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/change-password')
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('您的密码已经改变。')
            return redirect(url_for('main.index'))
        else:
            flash('密码输入错误')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset')
def password_reset_request():



@auth.route('/reset/<token>')
def password_reset():
    pass


@auth.route('/change-email')
def change_email_request():
    pass


@auth.route('/change-email/token')
def change_email():
    pass





