from flask import Blueprint, render_template

bp = Blueprint("auth", __name__)

@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")
    
@bp.route("/login")
def login():
    return render_template("auth/login.html")

