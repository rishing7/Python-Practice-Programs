from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My item',
                'price': 15.99
            }
        ]
    }
]
""" HTTP verbs definition server prospective since we are creating web server."""
# GET: To send data
# POST: To receive data
""" When POST request comes to server(our flask app) first look in the header(POST) to know which type of data is coming
 and then see what data is coming in body."""

""" Creating endpoints such that our serv"""


# POST /store data: {name}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data['name'],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>')  # http:127.0.0.1:5000/store/some_name
def get_store(name):
    # Iterate over stores
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({"message": "Store not found in stores"})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                "name": request_data['name'],
                "price": request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({"message": "Store name not found in stores"})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({"items": store['items']})
    return jsonify({"message": "Item not found in stores"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
