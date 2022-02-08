from . import BaseTestClass

from tfm.auth.models import User
from sqlite3 import ProgrammingError

class AppTestUserModel(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.valid_user = ('Jhon', 'Doe', 'jhon', 'jhon@email.com', 'Upplow$1234')
        self.required_fields_users = (
            ('', 'Doe', 'jhon', 'jhon@email.com', 'Upplow$1234'),
            ('Jhon', '', 'jhon', 'jhon@email.com', 'Upplow$1234'),
            ('Jhon', 'Doe', '', 'jhon@email.com', 'Upplow$1234'),
            ('Jhon', 'Doe', 'jhon', '', 'Upplow$1234'),
            ('Jhon', 'Doe', 'jhon', 'jhon@email.com', '')
        )
        self.valid_emails = (
            'example@email.com',
            'example.first.middle.lastname@email.com',
            'example@subdomain.email.com',
            'example+firstname+lastname@email.com',
            'example@234.234.234.234',
            'example@[234.234.234.234]',
            '0987654321@example.com',
            'example@email-one.com',
            '_______@email.com',
            'example@email.name',
            'example@email.museum',
            'example@email.co.jp',
            'example.firstname-lastname@email.com'
            # '“example”@email.com',
            # 'Valid Email Addresses that appear at glance to be invalid',
            # 'extremely.unusual.”@”.unusual.com@example.com',
            # 'very.”(),:;<>[]”.VERY.”very@\\ “very”.unusual@strange.email.example.com'
        )
        self.invalid_emails = (
            'plaintextaddress',
            '@#@@##@%^%#$@#$@#.com',
            '@email.com',
            'John Doe <example@email.com>',
            'example.email.com',
            'example@example@email.com',
            '.example@email.com',
            'example.@email.com',
            'example…example@email.com',
            'おえあいう@example.com',
            'example@email.com (John Doe)',
            # 'example@email',
            # 'example@-email.com',
            # 'example@email.web',
            # 'example@111.222.333.44444',
            'example@email…com',
            'CAT…123@email.com',
            '”(),:;<>[\]@email.com',
            'obviously”not”correct@email.com',
            'example\ is”especially”not\allowed@email.com'
        )
        self.valid_passwords = (
            'UPPERlower$/1',
            '%@@123uL',
            'UPPERlower$123__'
        )
        self.invalid_passwords = (
            'ALLUPPER',
            'alllower',
            '@#__%&///',
            '123456789',
            'Sh0rt$'
            'V3ry__large_pa$$w0rd'
        )


    def test_load_user(self):
        with self.app.app_context():
            user = User()

        self.assertIsInstance(user, User)
        with self.assertRaises(ProgrammingError) as e:
            user._db.execute('SELECT 1;')

        self.assertIn('closed', str(e.exception))
        self.assertEqual(user.messages, [])


    def test_create_valid_user(self):
        with self.app.app_context():
            user = User()
            user.create_user(*self.valid_user)

            self.assertEqual(user.messages, [])

    def test_create_user_without_required_fields(self):
        with self.app.app_context():
            user = User()
            for fields in self.required_fields_users:
                user.create_user(*fields)

                with self.assertRaises(AttributeError):
                    user.last_name

                self.assertEqual(user.messages[0], 'Required fields empty.')


    def test_create_user_with_valid_email(self):
        with self.app.app_context():
            for i, email in enumerate(self.valid_emails):
                user = User()
                user.create_user(f'Jhon{i}', f'Doe{i}', f'jhon{i}', email, 'Upplow$1234')

                self.assertEqual(user.messages, [])


    def test_create_user_with_invalid_email(self):
        with self.app.app_context():
            for i, email in enumerate(self.invalid_emails):
                user = User()
                user.create_user(f'Jhon{i}', f'Doe{i}', f'jhon{i}', email, 'Upplow$1234')

                self.assertEqual(user.messages, ['Invalid Email.'])


    def test_create_user_with_valid_password(self):
        with self.app.app_context():
            for i, password in enumerate(self.valid_passwords):
                user = User()
                user.create_user(f'Jhon{i}', f'Doe{i}', f'jhon{i}', f'user{i}@email.com', password)

                self.assertEqual(user.messages, [])


    def test_create_user_with_invalid_password(self):
        with self.app.app_context():
            for i, password in enumerate(self.invalid_passwords):
                user = User()
                user.create_user(f'Jhon{i}', f'Doe{i}', f'jhon{i}', f'user{i}@email.com', password)

                self.assertEqual(user.messages, ['Invalid Password.'])



    def test_find_user_by_email(self):
        with self.app.app_context():
            user = User()
            user.create_user(*self.valid_user)
            found = user.find_by_email('jhon@email.com')

            self.assertEqual(found['first_name'], 'Jhon')


    def test_find_user_by_email_invalid_email(self):
        with self.app.app_context():
            user = User()
            found = user.find_by_email('missing_mail')

            self.assertFalse(found)


    def test_email_uniqueness(self):
        with self.app.app_context():
            user1 = User()
            user1.create_user(*self.valid_user)
            user2 = User()
            user2.create_user(*self.valid_user)

            with self.assertRaises(AttributeError):
                    user2.first_name
            self.assertIn('already registered', user2.messages[0])


    def test_find_user_by_id(self):
        with self.app.app_context():
            user = User()
            user.create_user(*self.valid_user)
            found_by_email = user.find_by_email('jhon@email.com')
            found_by_id = user.find_by_id(found_by_email['id'])

            self.assertEqual(found_by_id['first_name'], 'Jhon')


    def test_find_user_by_id_invalid_id(self):
        with self.app.app_context():
            user = User()
            found = user.find_by_id('missing_id')

            self.assertFalse(found)
