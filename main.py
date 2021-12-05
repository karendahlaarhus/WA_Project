from flask import Blueprint, render_template
import flask_login 

bp = Blueprint("main", __name__)

@bp.route("/")
@flask_login.login_required
def index():
    return render_template("main/index.html")

