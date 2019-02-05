from flask import jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3


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
        # """ filter keeps iterating items, next gives only one item, None if no item is not in DB"""
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        """ Interaction with database."""
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found.'}, 404

    @classmethod
    def find_by_name(cls, name):
        """ Interaction with database."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        """ if server(my app) is not sure whether client is going to give me data or not then use argument of
        get_json(force:True) also dangerous as well as get_json(silent=True)"""
        # data = request.get_json() Usage of parser.

        if self.find_by_name(name):
            return {'message': "An item with {} is already exists.".format(
                name)}, 400  # A bad request which is client fault

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'message': 'An error occurred inserting the item'}
        return item, 201  # When server returns some data and everything is ok, 202 item is created but not getting soon

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item is deleted.'}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        data = Item.parser.parse_args()
        item = {'name': item['name'], 'price': data['price']}
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def put(self, name):  # Idempotent, output never change after calling multiple times.
        """ This method is put i.e if item exists then it updates that item otherwise creates new item. According to
        logic written below it can update name as well if we put the name that's why we are using reqparser."""
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        print(updated_item, item)
        if item:
            self.insert(updated_item)
        else:
            self.update(updated_item)

        return updated_item , 201

    @classmethod
    def update(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?)"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.commit()
        connection.close()
        return {'items': items}
