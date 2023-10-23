from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # == import db from __init__.py
from flask_login import login_required, logout_user, current_user
from .models import User
from . import created_mail
from flask_mail import Message


auth = Blueprint('auth', __name__)


@auth.route('/user_page')
def user_page():
    new_user = request.args.get('new_user')[2:-3]
    return render_template('page_user.html', new_user=new_user)


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
                new_user = User.query.filter_by(email=email).with_entities(User.first_name).first()
                return redirect(url_for("auth.user_page", new_user=new_user))
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
            return redirect(url_for('auth.user_page'))

    return render_template('Register.html')

@auth.route('/lobby')
def lobby():
    render_template("lobby.html")

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password_1():
    if request.method == 'POST':
        mail = created_mail()
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        global user_email
        user_email = email
        if user:
            #check email to our database
            msg = Message("Hey",
                sender='test@gmail.com',
                recipients=[email])
            msg.html = render_template("email.html")
            mail.send(msg)
            return "<h1>Sented</h1>"
        else:
            return "<h1>EMAIL NOT MATCH TO OUR DATABASE</h1>"
    return render_template("forgot_password_first.html")


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    password1 = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if password1 == password2:
            user = User.query.filter_by(email=user_email).first()
            if user:
                hashed_pass = generate_password_hash(password1, method='sha256')
                user.password = hashed_pass
                db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template("page_user.html")
    return render_template("reset_password.html")

