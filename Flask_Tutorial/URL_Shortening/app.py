from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from Programing.URL_Shortening.security import authenticate, identity
from Programing.URL_Shortening.resources.user import UserRegister
from Programing.URL_Shortening.resources.url import URL_Resource, URLRedirect

app = Flask(__name__)

""" Where to define data.db ? """
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/data'    #  "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

app.secret_key = 'rishi'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # Creates an endpoint i.e called /auth returns jw token.

api.add_resource(URL_Resource, '/')
api.add_resource(URLRedirect, '/<string:shortURL>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from Programing.URL_Shortening.db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
