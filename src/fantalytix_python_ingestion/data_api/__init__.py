from flask import Flask
from flask_marshmallow import Marshmallow

from fantalytix_sqlalchemy.orm.settings import CONNECTION

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = CONNECTION

    ma = Marshmallow(app)

    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    return app
