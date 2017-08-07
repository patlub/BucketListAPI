from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import application_config

db = SQLAlchemy()
db.create_all()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(application_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
