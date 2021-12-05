import flask_login
from . import db


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(100), nullable=False)
    # reservations = db.relationship('Reservation', backref='user', lazy=False)

""" class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    synopsis = db.Column(db.String(500), nullable = False)
    duration = db.Column(db.String(100), nullable = False)
    director = db.Column(db.String(64), nullable = False)
    leading_actor = db.Column(db.String(128), nullable = True)
    
class Screen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    
class Projection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"), nullable=False)
    datetime = db.Column(db.DateTime(), nullable=False)
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    projection_id = db.Column(db.Integer, db.ForeignKey("projection.id"), nullable=False)
    seats = db.Column(db.String(64), nullable = False)
    timestamp = db.Column(db.String(100), nullable=False) """