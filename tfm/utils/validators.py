import re

def validate_presence(*fields):
    return all(fields)

def validate_length(field, *limits):
    if validate_presence(limits):
        try:
            if len(limits) == 1:
                _min = limits[0]
                return _min <= len(field)
            else:
                _min, _max = limits
                return _min <= len(field) <= _max
        except Exception:
            return None
    return None

def validate_password(password):
    '''
    Password must have:
        length {8, 20}
        at least iclude one digit
        at least iclude one lowercase letter
        at least iclude one uppercase letter
        at least iclude one special character
    '''
    reg = '^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
    return re.search(re.compile(reg), password)

def validate_email(email):
    # TODO strong email regex
    reg = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    return re.fullmatch(reg, email)



