from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # == import db from __init__.py
from flask_login import login_required, logout_user, current_user
from .models import User, room
from . import created_mail, create_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


auth = Blueprint('auth', __name__)



@auth.route('/user_page', methods=['GET', 'POST'])
def user_page():
    user = request.args.get('new_user')
    all_data_user = room.query.filter_by(first_name=user).all()
    all_room = []
    if all_data_user:
        for data in all_data_user:
            groupname_user = data.groupname
            grouppassword_user = data.grouppassword
            selectedDate_user = data.selectedDate
            all_room.append([groupname_user, grouppassword_user, selectedDate_user])
    if request.method == 'POST':
        groupname = request.form.get('groupname')
        grouppassword = request.form.get('grouppassword')
        selectedDate = request.form.get('selectedDate')
        if groupname and grouppassword and selectedDate:
            flash("Successfully created a room", category=1)
            new_room = room(groupname=groupname, grouppassword=grouppassword, selectedDate=selectedDate, first_name=user)
            db.session.add(new_room)
            db.session.commit()
            return redirect(url_for('auth.user_page', new_user=user, methods=0))
        elif not groupname:
            flash("Please enter the room name.", category=0)
        elif not grouppassword:
            flash("Please enter the room code.", category=0)
        elif not selectedDate:
            flash("Please select a date.", category=0)
    return render_template('page_user.html', user=user, all_room=all_room)

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
                return redirect(url_for("auth.user_page", new_user=new_user[0]))
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
            return redirect(url_for('auth.login'))

    return render_template('Register.html')

@auth.route('/lobby')
def lobby():
    render_template("lobby.html")


#make token to reset password
def generate_reset_token(email):
    app = create_app()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='reset-password')


#if time > 3600 it need to resented
def validate_reset_token(token):
    app = create_app()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    max_age = 3600  # The token is valid for one hour (adjust as needed)
    try:
        email = serializer.loads(token, salt='reset-password', max_age=max_age)
        return email
    except:
        return None



@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password_1():
    if request.method == 'POST':
        mail = created_mail()
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            #check email to our database
            msg = Message("Hey",
                sender='test@gmail.com',
                recipients=[email])
            #get token = email
            token = generate_reset_token(email)
            #make reset link for email
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            msg.html = render_template("email.html", reset_link=reset_link)
            mail.send(msg)
            flash("Password reset link sent to your email.", category=0)
        else:
            flash("Email not match to our database", category=1)
    return render_template("forgot_password_first.html")


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = validate_reset_token(token)#get token from forgotpass
    if request.method == 'POST':
        password1 = request.form.get('password')
        password2 = request.form.get('password2')
        if password1 == password2:
            user = User.query.filter_by(email=email).first()
            if user:
                hashed_pass = generate_password_hash(password1, method='sha256')
                user.password = hashed_pass
                db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template("page_user.html")
    return render_template("reset_password.html")

