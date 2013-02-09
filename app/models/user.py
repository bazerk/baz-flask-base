from sqlalchemy.exc import IntegrityError
from app.database import db
import common


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)

    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(200))
    joined = db.Column(db.DateTime, default=common.now)

    twitter_oauth_token = db.Column(db.String(200))
    twitter_oauth_secret = db.Column(db.String(200))
    twitter_username = db.Column(db.String(80), unique=True)
    twitter_id = db.Column(db.String(200))

    def __init__(self, username, email, password_hash, twitter_deets=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        if twitter_deets:
            self.twitter_id = twitter_deets['user_id']
            self.twitter_username = twitter_deets['screen_name']
            self.twitter_oauth_token = twitter_deets['oauth_token']
            self.twitter_oauth_secret = twitter_deets['oauth_token_secret']

    @classmethod
    def create(cls, username, email, password_hash, twitter_deets=None):
        try:
            new_user = User(username, email, password_hash, twitter_deets)
            db.session.add(new_user)
            db.session.commit()
            return None, new_user
        except IntegrityError:
            db.session.rollback()
            return 'Username or email already exists', None

    @classmethod
    def authenticate(cls, login, password, check_hash_func):
        u = User.query.filter_by(username=login).scalar()
        if not u:
            u = User.query.filter_by(email=login).scalar()
            if not u:
                return None
        if check_hash_func(u.password_hash, password):
            return u
        return None

    @classmethod
    def from_twitter(cls, screen_name):
        return User.query.filter_by(twitter_username=screen_name).scalar()

    def __repr__(self):
        return "<User('{0}', '{1}', '{2}')>".format(self.id, self.username, self.password_hash)
