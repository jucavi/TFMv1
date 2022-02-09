from flask import Flask

def create_app(environment='development'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config.get(environment))

    @app.route('/hello')
    def hello():
        return 'Hello Flask!'

    from . import db
    db.init_app(app)

    from .auth import auth
    app.register_blueprint(auth.bp)

    return app
