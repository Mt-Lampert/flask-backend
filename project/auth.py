
class User(object):
    def __init__(self, _id, _name, _passwd) -> None:
        self.id = _id
        self.name = _name
        self.passwd = _passwd

    def __str__(self) -> str:
        return f"User(id='{self.id}')"


users = [
    User(1, "Mario", "abcd"),
    User(2, "Peach", "bcde"),
    User(3, "Yoshi", "cdef"),
]

username_table = {u.name: u for u in users}
uid_table = {u.id: u for u in users}


def authenticate(_name, _passwd):
    """
    GIVEN _name and _password,
    WHEN _name and _password are OK
    THEN the user from 'users' is returned
    """
    user = username_table.get(_name, None)
    if user and user.passwd.encode('utf-8') == _passwd.encode('utf-8'):
        return user


def identity(payload):
    """
    GIVEN a payload containing the ID of a user in payload['identiity']
    WHEN that ID is found in 'uid_table'
    THEN the user with that identity is returned.
    """
    user_id = payload['identity']
    return uid_table.get(user_id, None)
