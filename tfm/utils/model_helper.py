from functools import wraps
from sqlite3 import IntegrityError

def save_execute(func):
    wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            cls, *_ =  args
            if hasattr(cls, 'messages'):
                _, field = e.args[0].split()[-1].split('.')
                cls.messages.append(f'{field.capitalize()} is already registered.')
        except Exception as e:
            cls, *_ =  args
            if hasattr(cls, 'messages'):
                cls.messages.append(str(e))
            print(e)
    return wrapper