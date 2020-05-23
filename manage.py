import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user, blacklist, product, category, checkout, callto

app = create_app(os.getenv('MEDTRADING_ENV') or 'dev')
# app.register_blueprint(api, url_prefix='/api/1')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()

if __name__ == '__main__':
    manager.run()
