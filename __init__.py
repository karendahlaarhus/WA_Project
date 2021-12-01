from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = ""
    app.config["SQLALCHEMY_DATABASE_URI"] = ""



    from . import main
    app.register_blueprint(main.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app