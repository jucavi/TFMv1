import unittest

from tfm import create_app

class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(environment='testing')
        # self.ctx = self.app.app_context()
        # self.ctx.push()
        self.start_db()

        # with self.ctx:
        #     pass

    def tearDown(self):
        self.start_db()
        # with self.ctx:
        #     pass


    def start_db(self):
        runner = self.app.test_cli_runner()
        runner.invoke(args=['start-db'])