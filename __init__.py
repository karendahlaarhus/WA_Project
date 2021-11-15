from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    from . import main
    app.register_blueprint(main.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app