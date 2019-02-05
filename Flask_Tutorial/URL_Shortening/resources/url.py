from flask_jwt import jwt_required, request
from Programing.URL_Shortening.coversion import IdToShortURL
from flask_restful import Resource
from Programing.URL_Shortening.models.url import URLModel
from flask import redirect


class URL_Resource(Resource):

    def post(self):
        """ if server(my app) is not sure whether client is going to give me data or not then use argument of
        get_json(force:True) also dangerous as well as get_json(silent=True)"""

        data = request.get_json()
        if URLModel.find_by_name(data['originalURL']):
            item = URLModel.find_by_name(data['originalURL'])
            return item.json()['shortURL']
        rows = URLModel.query.all()
        id = len(rows)
        shortURL = IdToShortURL.idToShortURL(id)
        item = URLModel(data['originalURL'], shortURL)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}
        return shortURL


class URLRedirect(Resource):
    # @jwt_required
    def get(self, shortURL):
        item = URLModel.find_by_shortURL(shortURL)
        return redirect(item.json()['originalURL'])

