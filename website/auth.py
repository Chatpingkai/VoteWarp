from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # == import db from __init__.py
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # login_user(user, remember=True)
                return render_template("lobby.html")
            else:
                flash('Incorrect Password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash("Don't joke to me put ur real email", category='error')
        elif len(first_name) < 2:
            flash("Yo! Bro we think ur name is to short!! EiEi -3-", category='error')
        elif len(password1) < 8:
            flash("YoYo Ur pass too weak make them power up pls", category='error')
        elif password1 != password2:
            flash("Are u got a problem about remember?? It's Not Match", category='error')
        
        else:
            # add user to our database <3
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash("Account Created!! enjoy kub pom", category='success')
            return render_template('login.html')

    return render_template('Register.html')

@auth.route('/lobby')
def lobby():
    render_template("lobby.html")
