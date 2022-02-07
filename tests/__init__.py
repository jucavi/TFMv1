import unittest

from tfm import create_app

class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(environment='testing')

        with self.app.app_context():
            pass

    def tearDown(self):
        with self.app.app_context():
            pass