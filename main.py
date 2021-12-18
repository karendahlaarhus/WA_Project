import datetime
from os import abort
import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login 
from . import db, model

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    movies = model.Movie.query.order_by(model.Movie.title).all()
    now = datetime.datetime.now()
    projections = model.Projection.query.filter(model.Projection.datetime.between(
        now, now+datetime.timedelta(days=3))).order_by(model.Projection.datetime).all()

    return render_template("main/index.html", movies=movies, projections=projections)

@bp.route("/movies/<int:movie_id>")
def movie_view(movie_id):
    movie = model.Movie.query.filter_by(id=movie_id).first()
    projections = model.Projection.query.filter_by(movie_id=movie_id).all()
    if not movie:
        abort(404,"Movie id {} doesn't exist".format(movie_id))
    return render_template("main/movie_view.html", movie=movie, projections=projections)


@bp.route("/projections/<int:projection_id>")
@flask_login.login_required
def projection_view(projection_id):
    
    user_id = flask_login.current_user.id
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())

    projection = model.Projection.query.filter(model.Projection.id == projection_id).one()
    sum_result = db.session.query(db.func.sum(model.Reservation.seats).label('reserved')).filter(model.Reservation.projection == projection).one()
    reserved_seats = sum_result.reserved
    if reserved_seats is None:
        reserved_seats = 0
    free_seats = projection.screen.available_seats - reserved_seats

    if not projection:
        abort(404,"Movie id {} doesn't exist".format(projection_id))
    return render_template("main/projection_view.html", projection=projection, free_seats=free_seats)

    

@bp.route("/projection/<int:projection_id>", methods=["POST"])
@flask_login.login_required
def make_reservation(projection_id):
    
    user_id = flask_login.current_user.id
    seats = int(request.form.get("seats"))
    timestamp = datetime.datetime.now(dateutil.tz.tzlocal())

    projection = model.Projection.query.filter(model.Projection.id == projection_id).one()
    sum_result = db.session.query(db.func.sum(model.Reservation.seats).label('reserved')).filter(model.Reservation.projection == projection).one()
    reserved_seats = sum_result.reserved
    if reserved_seats is None:
        reserved_seats = 0
    free_seats = projection.screen.available_seats - reserved_seats

    if free_seats < seats:
        flash("There are not enough available seats for this projection")
    else:
        reservation = model.Reservation(user_id=user_id, projection_id=projection_id, seats=seats, timestamp=timestamp)
        db.session.add(reservation)
        db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/reservations")
@flask_login.login_required
def reservations_view():
    user = flask_login.current_user
    reservations = model.Reservation.query.order_by(model.Reservation.timestamp).filter_by(user_id=user.id).all()
    return render_template("main/reservations_view.html", reservations=reservations, user=user)

@bp.route("/reservations/<int:reservation_id>")
@flask_login.login_required
def reservation_view(reservation_id):
    reservation = model.Reservation.query.filter_by(id=reservation_id).first()
    projection = model.Projection.query.filter_by(id=reservation.projection_id).first()
    movie = projection.movie

    return render_template("main/reservation_view.html", reservation=reservation, projection=projection, movie=movie)
