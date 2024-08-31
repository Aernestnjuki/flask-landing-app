from aiohttp.helpers import call_later
from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignUpForm, LoginForm
from .models import Register
from . import db
from flask_login import login_user, logout_user


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_user = Register()

            new_user.email = email
            new_user.username = username
            new_user.password = password2

            try:
                db.session.add(new_user)
                db.session.commit()
                flash("You have successfully registered", category='success')
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                flash('Registration failed', category='danger')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Register.query.filter_by(email=email).first()

        if user:
            if user.verify_password(password=password):
                login_user(user)
                flash('Successfully logged in', category='success')
                return redirect('/')
            else:
                flash('Password does not match', category='danger')
        else:
            flash('Account does not exist')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))