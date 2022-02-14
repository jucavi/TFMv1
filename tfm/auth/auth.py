from crypt import methods
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .models import User
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user = User()
        user.create_user(*request.form.values())
        if not user.messages:
            flash('User successfully registered')
            return redirect(url_for('auth.login'))
        flash(*user.messages)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print('In login')
        user = User()
        email = request.form['email']
        password = request.form['password']
        user.check_password(email, password)

        if not user.messages:
            session.clear()
            session['user_id'] = user.user['id']
            return render_template('index.html') #TODO use redirect


        flash(*user.messages)
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return render_template('index.html') #TODO use redirect


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id:
        g.user = User().find_by_id(user_id)
    else:
        g.user = None


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view