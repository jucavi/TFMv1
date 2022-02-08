from uuid import uuid4
from .. import db
from ..utils.validators import validate_email, validate_presence, validate_password
from ..utils.model_helper import save_execute

from werkzeug.security import check_password_hash, generate_password_hash

class User:
    def __init__(self):
        self._db = db.get_db()
        self._table = 'user'
        self.messages = []

    @save_execute
    def create_user(self, first_name, last_name, user_name, email, password):
        if not validate_presence(first_name, last_name, user_name, email, password):
            self.messages.append('Required fields empty.')
        if not validate_email(email):
            self.messages.append('Invalid Email.')
        if not validate_password(password):
            self.messages.append('Invalid Password.')
        if self.messages:
            return None
        self._db.cursor()
        user = (str(uuid4()), first_name, last_name, user_name, email, generate_password_hash(password))
        self._db.execute(f'INSERT INTO {self._table} VALUES (?, ?, ?, ?, ?, ?)', user)

    @save_execute
    def find_by_id(self, _id):
        user = self._db.execute(f'SELECT * FROM {self._table} WHERE id = ?', (_id, )).fetchone()
        return user


    @save_execute
    def find_by_email(self, email):
        user = self._db.execute(f'SELECT * FROM {self._table} WHERE email = ?', (email, )).fetchone()
        return user


    def check_password(self, password):
        if hasattr(self, 'password'):
            return check_password_hash(self.password, password)
