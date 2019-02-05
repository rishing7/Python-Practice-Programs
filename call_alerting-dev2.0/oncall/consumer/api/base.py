from flask_restful import Resource
from flask import jsonify
from common import api_exceptions
from flask import make_response


class ResourceView(Resource):
    """
    Resource View Base class which makes http response and customize the dispatch method
    on every request

    schema_class: Validation class for every API request endpoint
    model: DB class

    """
    schema_class = None
    model = None
    json_mime_type = 'application/json'

    @api_exceptions.api_exception_handler
    def dispatch_request(self, *args, **kwargs):
        return super(ResourceView, self).dispatch_request(*args, **kwargs)

    def jsonResponse(self, data, status=200, headers=None):
        headers = headers or {}
        if isinstance(data, dict):
            if 'Content-Type' not in headers:
                headers['Content-Type'] = self.json_mime_type
            return make_response(
                jsonify({
                    "response": data
                }), status, headers)
        else:
            raise api_exceptions.BadRequestData()


class ResourceGetPost(ResourceView):
    """
    Method handles GET, POST requests
    """

    def post(self, *args, **kwargs):
        return self.jsonResponse(**kwargs)

    def get(self, *args, **kwargs):
        return self.jsonResponse(**kwargs)


class ResourceRetrievePutDelete(ResourceView):
    """
    Method handles Retrieve,PUT,Delete requests
    """

    def get(self, *args, **kwargs):
        return self.jsonResponse(**kwargs)

    def put(self, *args, **kwargs):
        return self.jsonResponse(**kwargs)

    def delete(self, *args, **kwargs):
        return self.jsonResponse(**kwargs)
