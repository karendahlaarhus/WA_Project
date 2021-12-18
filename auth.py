from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from . import db, bcrypt, model

bp = Blueprint("auth", __name__)

@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")

@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    if password != request.form.get("password_repeat"):
        flash("The passwords you provided are not identical")
        return redirect(url_for("auth.signup"))

    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("The email you provided is already registereds")
        return redirect(url_for("auth.signup"))

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flask_login.login_user(new_user)
    return redirect(url_for("main.index"))
    
@bp.route("/login")
def login():
    return render_template("auth/login.html")

@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        flask_login.login_user(user)
        return redirect(url_for("main.index"))
    else:
        flash("Wrong email and/or password")
        return redirect(url_for("auth.login"))

@bp.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("auth.login"))

    
    
    


