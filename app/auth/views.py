from . import auth


@auth.route('/register')
def register():
    return "<h1> Resister </h1>"


@auth.route('/login')
def login():
    return "<h1>Login</h1>"


@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"


@auth.route('/confirm')
def resend_confirmation():
    pass

@auth.route('/confirm/<token>')
def confirm():
    pass


@auth.route('/unconfirmed')
def unconfirmed():
    pass


@auth.route('/change-password')
def change_password():
    pass


@auth.route('/reset')
def password_reset_request():
    pass


@auth.route('/reset/<token>')
def password_reset():
    pass


@auth.route('/change-email')
def change_email_request():
    pass


@auth.route('/change-email/token')
def change_email():
    pass





