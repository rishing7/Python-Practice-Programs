from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from Flask_Tutorial.Section6.code.security import authenticate, identity
from Flask_Tutorial.Section6.code.resources.user import UserRegister
from Flask_Tutorial.Section6.code.resources.item import Item, Items

app = Flask(__name__)

""" Where to define data.db. """
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# SQLALCHEMY creates data.db database but there is no table in it.

@app.before_first_request
def create_table():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # Creates an endpoint i.e called /auth returns jw token.


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from Flask_Tutorial.Section6.code.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
