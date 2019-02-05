from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from Flask_Tutorial.Section5.code.security import authenticate, identity
from Flask_Tutorial.Section5.code.user import UserRegister
from Flask_Tutorial.Section5.code.item import Items, Item

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # Creates an endpoint i.e called /auth returns jw token.


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
