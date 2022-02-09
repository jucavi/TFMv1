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
        user = (str(uuid4()), first_name, last_name, user_name, email, generate_password_hash(password))
        with self._db as con:
            con.execute(f'INSERT INTO {self._table} VALUES (?, ?, ?, ?, ?, ?)', user)
            con.commit()

    @save_execute
    def find_by_id(self, _id):
        with self._db as con:
            user = con.execute(f'SELECT * FROM {self._table} WHERE id = ?', (_id, )).fetchone()
        if user:
            return user
        self.messages.append('User not found.')


    @save_execute
    def find_by_email(self, email):
        with self._db as con:
            user = con.execute(f'SELECT * FROM {self._table} WHERE email = ?', (email, )).fetchone()
        if user:
            return user
        self.messages.append('User not found.')


    def check_password(self, email, password):
        user = self.find_by_email(email)
        if user:
            if check_password_hash(user['password'], password):
                return True
            else:
                self.messages.append('Wrong password.')
                return False