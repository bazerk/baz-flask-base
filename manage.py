from app import create_app, init_app, create_db, clear_db
from flask.ext.script import Manager

flask_app = create_app()
manager = Manager(flask_app)


@manager.command
def run(config=None):
    """Run local server."""
    init_app(flask_app, config)
    flask_app.run()


@manager.command
def cleardb(config=None):
    init_app(flask_app, config)
    clear_db(flask_app)


@manager.command
def initdb(config=None):
    """Create DB from scratch"""
    init_app(flask_app, config)
    create_db(flask_app)


if __name__ == "__main__":
    manager.run()
