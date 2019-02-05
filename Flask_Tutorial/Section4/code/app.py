from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from Flask_Tutorial.Section4.code.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # Creates an endpoint i.e called /auth returns jw token.

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field can't be left blank")
    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {'item': None}, 404  # If item is not found use 404 status code
        # OR
        """ filter keeps iterating items, next gives only one item, None if no item is not in DB"""
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        """ if server(my app) is not sure whether client is going to give me data or not then use argument of
        get_json(force:True) also dangerous as well as get_json(silent=True)"""
        # data = request.get_json() Usage of parser.

        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with {} is already exists.".format(
                name)}, 400  # A bad request which is client fault

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # When server returns some data and everything is ok, 202 item is created but not getting soon

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item is deleted.'}

    def put(self, name):  # Idempotent, output never change after calling multiple times.
        """ This method is put i.e if item exists then it updates that item otherwise creates new item. According to
        logic written below it can update name as well if we put the name that's why we are using reqparser."""
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': data['name'], 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class Items(Resource):
    def get(self):
        return jsonify({'items': items})


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
app.run(port=5000, debug=True)
