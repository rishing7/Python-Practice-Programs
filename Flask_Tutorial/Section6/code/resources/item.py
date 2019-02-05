from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from Flask_Tutorial.Section6.code.models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        """ if server(my app) is not sure whether client is going to give me data or not then use argument of
        get_json(force:True) also dangerous as well as get_json(silent=True)"""
        # data = request.get_json() Usage of parser.

        if ItemModel.find_by_name(name):
            return {'message': "An item with {} is already exists.".format(
                name)}, 400  # A bad request which is client fault

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}
        return item.json(), 201  # When server returns some data and everything is ok, 202 item is created but not getting soon

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_from_db(item)
        return {"message": "Item deleted"}

    def put(self, name):  # Idempotent, output never change after calling multiple times.
        """ This method is put i.e if item exists then it updates that item otherwise creates new item. According to
        logic written below it can update name as well if we put the name that's why we are using reqparser."""
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        # updated_item = ItemModel(name, data['price'])
        # print(updated_item, item)

        if item is None:
            # try:
            #     updated_item.insert()
            #
            # except:
            #     return {"message": "An error occurred while inserting the item."}, 500

            item = ItemModel(name, data['price'])

        else:
            # try:
            #     updated_item.update()
            # except:
            #     return {"message": "An error occurred while updating the item."}, 500

            item.price = ItemModel(name, data['price'])

        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # connection.commit()
        # connection.close()
        # return {'items': items}
        return {'ItemList': [item.json() for item in ItemModel.query.all()]}    # { 'itemList':list(map(lambda x: x.json(), ItemModel.query.all())}
