from flask import Flask, request, make_response

app = Flask(__name__)

myDB = [
    {'username': 'aaaa',
     'password': 'aaaa'
     },
    {'username': 'bbbb',
     'password': 'bbbb'
     },
    {'username': 'cccc',
     'password': 'cccc'
     },
]


@app.route('/')
def index():
    for item in myDB:
        if request.authorization and request.authorization.username == item[
            'username'] and request.authorization.password == item['password']:
            return "<h1>You are logged in!</h1>"
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/register', methods=['POST'])
def registerUser():
    data = request.get_json()
    item = {'username': data['username'], 'password': data['password']}
    myDB.append(item)
    return "User Registered Successfully!!!"


if __name__ == '__main__':
    app.run()
