from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_cors import CORS

from .config import config_by_name


class SQLiteAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options.update({
            'isolation_level': 'READ UNCOMMITTED',
        })
        super(SQLiteAlchemy, self).apply_driver_hacks(app, info, options)


db = SQLiteAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    mail.init_app(app)

    return app