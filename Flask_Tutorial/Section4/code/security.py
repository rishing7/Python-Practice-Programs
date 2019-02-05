from Flask_Tutorial.Section4.code.user import User
from werkzeug.security import safe_str_cmp

users = [
        User(1, 'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


# print(userid_mapping[1])

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password): # == is not used for string
        return user


def identity(payload):
    print(payload)
    user_id = payload['identity']

    return userid_mapping.get(user_id, None)