import unittest
from app import create_app, init_app, create_db, clear_db
from app.models import User


class AppBaseTest(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.project = create_app()
        init_app(self.project, 'test')
        self.app = self.project.test_client()
        with self.project.test_request_context():
            create_db(self.project)
            clear_db(self.project)

    def tearDown(self):
        pass

    def add_user(self):
        (err, user) = User.create('test', 'test@test.com', 'test')
        return user


from .models import *
from .routes import *
