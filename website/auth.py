from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # == import db from __init__.py
from flask_login import login_required, logout_user, current_user, login_user
from .models import User, room, Profile, vote
from . import created_mail, create_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from io import BytesIO


auth = Blueprint('auth', __name__)



@auth.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():
    user = request.args.get('new_user')
    all_data_user = room.query.filter_by(first_name=user).all()
    all_data_profile = Profile.query.filter_by(first_name=user).first()
    all_profile = []
    if all_data_profile:
        all_profile  = [all_data_profile.filepname, all_data_profile.filebname]
    all_room = []
    if all_data_user:
        for data in all_data_user:
            groupname_user = data.groupname
            grouppassword_user = data.grouppassword
            selectedDate_user = data.selectedDate
            picture_room = data.filename
            status = data.status
            grouppassword = data.grouppassword
            all_room.append([groupname_user, grouppassword_user, selectedDate_user, picture_room, status, grouppassword])
    if request.method == 'POST':
        groupname = request.form.get('groupname')
        grouppassword = request.form.get('grouppassword')
        selectedDate = request.form.get('selectedDate')
        picture_room = request.files['file']
        if groupname and grouppassword and selectedDate and picture_room:
            password = room.query.filter_by(grouppassword=grouppassword).first()
            if password == None and grouppassword.isalpha() and grouppassword.isupper() and len(grouppassword) == 4:
                flash("Successfully created a room", category=1)
                status = False
                new_room = room(groupname=groupname, grouppassword=grouppassword, selectedDate=selectedDate, filename=picture_room.filename, picture=picture_room.read(), status=status , first_name=user)
                db.session.add(new_room)
                db.session.commit()
                return redirect(url_for('auth.user_page', new_user=user, methods=0))
            elif not grouppassword.isupper() or len(grouppassword) != 4:
                flash("Please enter 4 capital letters.", category=0)
            else:
                flash("This Code room has already", category=0)
        elif not groupname:
            flash("Please enter the room name.", category=0)
        elif not grouppassword:
            flash("Please enter the room code.", category=0)
        elif not selectedDate:
            flash("Please select a date.", category=0)
        elif not picture_room:
            flash("Please select a picture.", category=0)
    return render_template('page_user.html', user=user, all_room=all_room, all_profile=all_profile, as_attachment=True)

@auth.route('/download_picture/<filename>')
@login_required
def download_picture(filename):
    data = room.query.filter_by(filename=filename).first()
    return send_file(BytesIO(data.picture), mimetype='image/jpeg', download_name=filename, as_attachment=True)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
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
    return redirect(url_for('auth.login'))


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
        elif User.query.filter_by(first_name=first_name) != "":
            flash("This name has already", category='error')
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
            msg = Message("Forgot password link",
                sender='Votewarp@gmail.com',
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

@auth.route('/Profile/<user>', methods=['GET', 'POST'])
@login_required
def profile(user):
    data = Profile.query.filter_by(first_name=user).first()
    all_data_profile = Profile.query.filter_by(first_name=user).first()
    all_profile = []
    if all_data_profile:
        all_profile  = [all_data_profile.filepname, all_data_profile.filebname]
    if request.method == 'POST':
        first_name = user
        picturep = request.files['picturep']
        pictureb = request.files['pictureb']
        if data == None:
            if picturep and pictureb:
                addpicture = Profile(filepname=picturep.filename, picturep=picturep.read(), filebname=pictureb.filename, pictureb=pictureb.read(), first_name=first_name)
                db.session.add(addpicture)
            else:
                flash("Please edit both of your profile and backgroound", category=0)
                return render_template("edit_profile.html", user=user, all_profile=all_profile)
        elif picturep.filename != "":
            data.picturep = picturep.read()
            data.filepname = picturep.filename
        elif pictureb.filename != "": 
            data.pictureb = pictureb.read()
            data.filebname = pictureb.filename
        db.session.commit()
        return redirect(url_for('auth.user_page', new_user=user))
    return render_template("edit_profile.html", user=user, all_profile=all_profile)

@auth.route('/download_pictureb/<filename>')
@login_required
def pictureb(filename):
    data = Profile.query.filter_by(filebname=filename).first()
    return send_file(BytesIO(data.pictureb), mimetype='image/jpeg', download_name=filename, as_attachment=True)

@auth.route('/download_picturep/<filename>')
@login_required
def picturep(filename):
    data = Profile.query.filter_by(filepname=filename).first()
    return send_file(BytesIO(data.picturep), mimetype='image/jpeg', download_name=filename, as_attachment=True)


@auth.route('/room/<grouppassword>', methods=['GET', 'POST'])
@login_required
def voteroom(grouppassword):
    if not Profile.query.filter_by(first_name=grouppassword[4:]).first():
        flash("Please edit your profile and backgroound", category=0)
        return redirect(url_for('auth.user_page', new_user=grouppassword[4:]))
    data = room.query.filter_by(grouppassword=grouppassword[:4]).first()
    roomname = data.groupname
    all_vote = vote.query.filter_by(grouppassword=grouppassword[:4]).all()
    list_vote = []
    if all_vote:
        for data in all_vote:
            place = data.place
            time = data.time
            description = data.description
            votename = data.votename
            if votename != "":
                votename = votename.split()
            picturename = data.filename
            list_vote.append([place, time, description, votename, picturename])
    if request.method == 'POST':
        place = request.form.get('place')
        time = request.form.get('time')
        description = request.form.get('descrip')
        picture = request.files['votepic']
        votename = ""
        sameplace = ""
        for i in vote.query.filter_by(grouppassword=grouppassword[:4]).all():
            if i.place == place:
                sameplace = i.place
        if place and time and description and sameplace != place:
            add_vote = vote(grouppassword=grouppassword[:4], place=place, time=time, description=description, filename=picture.filename, picture=picture.read(),  votename=votename)
            db.session.add(add_vote)
            db.session.commit()
            return redirect(url_for('auth.voteroom', grouppassword=grouppassword))
        elif sameplace == place:
            flash("This place has already")
        elif not place:
            flash("Please enter the location")
        elif not time:
            flash("Please enter time")
        elif not description:
            flash("Please enter description.")
    return render_template("room.html", grouppassword=grouppassword, roomname=roomname, list_vote=list_vote)

@auth.route('/find/<user>', methods=['GET', 'POST'])
@login_required
def find(user):
    password = request.form.get("search")
    password2 = room.query.filter_by(grouppassword=password).first()
    if request.method == "POST":
        if password2:
            if password == password2.grouppassword:
                password = password+user
                return redirect(url_for('auth.voteroom', grouppassword=password))
            else:
                flash("Don't have This room code", category=0)
        else:
            flash("Don't have This room code", category=0)
    return redirect(url_for('auth.user_page', new_user=user, methods=0))

@auth.route('/test/<data>', methods=['GET', 'POST'])
@login_required
def test(data):
    list_data = data.split(",")
    all_vote = vote.query.filter_by(grouppassword=list_data[0][:4]).all()
    for whatvote in all_vote:
        if whatvote.place == list_data[1] and whatvote.time == list_data[2] and list_data[0][4:] not in whatvote.votename:
            whatvote.votename = whatvote.votename+list_data[0][4:]+" "
        elif whatvote.place == list_data[1] and whatvote.time == list_data[2] and list_data[0][4:] in whatvote.votename:
            whatvote.votename =  (whatvote.votename).replace(list_data[0][4:], "")
    db.session.commit()
    return redirect(url_for('auth.voteroom', grouppassword=list_data[0]))

@auth.route('/download_vote/<filename>')
@login_required
def votepicture(filename):
    data = vote.query.filter_by(filename=filename).first()
    return send_file(BytesIO(data.picture), mimetype='image/jpeg', download_name=filename, as_attachment=True)

@auth.route('/votepro/<user>')
@login_required
def votepro(user):
    data = Profile.query.filter_by(first_name=user).first()
    if data:
        return send_file(BytesIO(data.picturep), mimetype='image/jpeg', download_name=data.filepname, as_attachment=True)
