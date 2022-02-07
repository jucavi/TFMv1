from . import BaseTestClass

from sqlite3 import ProgrammingError
from tfm.db import get_db

class AppTestDB(BaseTestClass):
    def test_get_close_db(self):
        with self.app.app_context():
            db = get_db()
            self.assertEqual(db, get_db())

        with self.assertRaises(ProgrammingError) as e:
            db.execute('SELECT 1;')

        self.assertIn('closed', str(e.exception))


    def test_init_db_command(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['start-db'])
        self.assertIn('Initialized', result.output)
