import datetime
from os import abort
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login 
from . import db, model

bp = Blueprint("main", __name__)

@bp.route("/")
@flask_login.login_required
def index():
    movies = model.Movie.query.order_by(model.Movie.title).all()
    projections = model.Projection.query.order_by(model.Projection.id).all()
    return render_template("main/index.html", movies=movies, projections=projections)


@bp.route("/reservations")
@flask_login.login_required
def reservations():
    reservations = model.Reservation.query.order_by(model.Reservation.timestamp).all()
    return render_template("main/reservations.html", reservations=reservations)


@bp.route("/movies/<int:movie_id>")
@flask_login.login_required
def movie_view(movie_id):
    movie = model.Movie.query.filter_by(id=movie_id).first()
    if not movie:
        abort(404,"Movie id {} doesn't exist".format(movie_id))
    return render_template("main/movie_view.html", movie=movie)


@bp.route("/projections/<int:projection_id>")
@flask_login.login_required
def projection_view(projection_id):
    projection = model.Projection.query.filter_by(id=projection_id).first()
    if not projection:
        abort(404,"Movie id {} doesn't exist".format(projection_id))
    return render_template("main/projection_view.html", projection=projection)

@bp.route("/projection/<int:projection_id>", methods=["POST"])
@flask_login.login_required
def make_reservation(projection_id):
    """How can i get the user id of current user?"""
    user_id = request.form.get("user_id")
    seats = request.form.get("seats")
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
   
    reservation = model.Reservation(user_id=user_id, projection_id=projection_id, seats=seats, timestamp=timestamp)
    db.session.add(reservation)
    db.session.commit()
    return render_template("main/index.html")