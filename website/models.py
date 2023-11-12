from . import db
from website import create_app
from flask_login import UserMixin
# from sqlalchemy.sql import func
from itsdangerous import URLSafeSerializer as Serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(150))
    grouppassword = db.Column(db.String(150))
    selectedDate = db.Column(db.String(150))
    filename = db.Column(db.String(150))
    picture = db.Column(db.LargeBinary)
    status = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepname = db.Column(db.String(150))
    picturep = db.Column(db.LargeBinary)
    filebname = db.Column(db.String(150))
    pictureb = db.Column(db.LargeBinary)
    first_name = db.Column(db.String(150))

class vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grouppassword = db.Column(db.String(150))
    place = db.Column(db.String(150))
    time = db.Column(db.String(150))
    description = db.Column(db.String(150))
    filename = db.Column(db.String(150))
    picture = db.Column(db.LargeBinary)
    votename = db.Column(db.String(150))
