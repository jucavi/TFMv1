from crypt import methods
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .models import User
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User()
        user.create_user(*request.form.values())
        if not user.messages:
            flash('User successfully registered')
            return redirect(url_for('auth.login'))
        flash(*user.messages)
    return render_template('auth/register.html')


@bp.route('/login')
def login():
    return 'Log In!'
