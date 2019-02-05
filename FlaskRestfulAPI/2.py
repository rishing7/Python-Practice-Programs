from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def post(self, todo_id):
        data = request.get_json()
        print(data)
        todos[data[todo_id]] = data['value']
        return {'msg': "{} and {} are added".format(data[todo_id], data['value'])}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
