from flask_restful import Resource, reqparse
from Programing.URL_Shortening.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field can't be left blank")
    parser.add_argument('password', type=str, required=True, help="This field can't be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username with {} already exists.".format(data['username'])}, 400

        user = UserModel(**data)  # data['username'], data['password']
        user.save_to_db()

        return {"message": "User created successfully"}, 201
