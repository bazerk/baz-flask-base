from flask import Flask, session, render_template, g

import extensions
from .configs import get_config
from .frontend import frontend
from .admin import admin
from .database import db
from .models import User

blueprints = (
    (frontend, None),
    (admin, '/admin')
)


def create_app():
    app = Flask(__name__)
    return app


def init_app(app, config=None):
    configure_app(app, config)
    configure_db(app)
    configure_assets(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_request_handlers(app)
    configure_error_handlers(app)


def configure_app(app, config_name):
    config = get_config(config_name)
    app.config.from_object(config)
    project = app.config['PROJECT'].upper()
    app.config.from_envvar('%s_APP_CONFIG' % project, silent=True)


def configure_db(app):
    db.init_app(app)


def configure_assets(app):
    from flask.ext.assets import Environment, Bundle
    assets = Environment(app)
    js = Bundle('js/vendor/jquery-1.9.0.min.js', 'js/vendor/underscore.min.js',
                'js/vendor/bootstrap.min.js', 'js/vendor/backbone.min.js',
                'js/controllers/base.js',
                filters='jsmin', output='gen/packed.js')
    assets.register('js_all', js)
    css = Bundle('css/bootstrap.min.css', 'css/bootstrap-responsive.min.css', 'css/style.css',
                 filters='cssmin', output='gen/packed.css')
    assets.register('css_all', css)


def configure_extensions(app):
    extensions.bcrypt.init_app(app)
    extensions.twitter.set_callback('%s/login-twitter-callback' % app.config['URL_BASE'])
    extensions.twitter.set_keys(app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET'],
        app.config['TWITTER_ACCESS_TOKEN_KEY'], app.config['TWITTER_ACCESS_TOKEN_SECRET'])

    import memcache
    mc = memcache.Client([app.config['MEMCACHED_STORE']], debug=0)

    from simplekv.memory.memcachestore import MemcacheStore
    from flaskext.kvsession import KVSessionExtension
    store = MemcacheStore(mc)
    KVSessionExtension(store, app)


def configure_blueprints(app):
    for (blueprint, url_prefix) in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_request_handlers(app):
    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            g.user = User.query.filter_by(id=session['user_id']).first()


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        return render_template("errors/405.html"), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500


def create_db(app):
    db.create_all()


def clear_db(app):
    User.query.delete()
    db.session.commit()
