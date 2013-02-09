import os


class BaseConfig(object):

    # Get app root path
    _basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    PROJECT = "flask-project"
    DEBUG = False
    TESTING = False

    ADMINS = frozenset(['support@support.net'])

    SECRET_KEY = 'Change this to something'

    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET = ''

    TWITTER_ACCESS_TOKEN_KEY = ''
    TWITTER_ACCESS_TOKEN_SECRET = ''

    URL_BASE = 'http://localhost:5000'

    MEMCACHED_STORE = '127.0.0.1:11211'

    # ===========================================
    # Flask-mail
    #
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'gmail_username'
    MAIL_PASSWORD = 'gmail_password'
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME

    # ===========================================
    # Flask-babel
    #
    ACCEPT_LANGUAGES = ['zh']
    BABEL_DEFAULT_LOCALE = 'en'

    # ===========================================
    # Flask-cache
    #
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60


class ProdConfig(BaseConfig):

    DEBUG = False
    URL_BASE = 'http://myprodurl.com'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@server/dbname'


class DevConfig(BaseConfig):

    DEBUG = True

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@server/dbname'


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


configs = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}


def get_config(config=None):
    if config in configs:
        return configs[config]()
    return DevConfig
