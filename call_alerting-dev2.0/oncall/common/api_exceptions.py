from functools import wraps
from flask import make_response
from flask import jsonify

JSON_MIME_TYPE = 'application/json'


# most exception classes are a blatant ripoff, just shaved off some stuff:
# https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/exceptions.py
# exception_handler is a homegrown decorator,
# different from how DRF handles it.


def api_exception_handler(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except APIException as e:
            return jsonResponse(
                {'error': str(e.detail), 'status_code': e.code},
                e.code)

    return decorated_function


def jsonResponse(data, status=200, headers=None):
    headers = headers or {}
    if isinstance(data, dict):
        if 'Content-Type' not in headers:
            headers['Content-Type'] = JSON_MIME_TYPE
        return make_response(
            jsonify({
                "response": data
            }), status, headers)
    else:
        raise BadRequestData()


class APIException(Exception):
    """
       Base class for API exceptions.
       Subclasses should provide `.status_code` and `.default_detail` properties.
       """
    # default - for unhandled exceptions - should ideally never happen, since
    # these will be mostly raised by devs themselves while handling requests.
    status_code = 500
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None, errors=None, code=None):

        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail
        # self.errors = errors
        if code is None:
            self.code = self.status_code
        else:
            self.code = code

    def __str__(self):
        return self.detail


class BadRequestData(APIException):
    status_code = 400
    default_detail = 'Bad request data.'


class ParseError(APIException):
    status_code = 400
    default_detail = 'Malformed request.'


class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'Incorrect authentication credentials.'


class NotAuthenticated(APIException):
    status_code = 401
    default_detail = 'Authentication credentials were not provided.'


class PermissionDenied(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'


class NotFound(APIException):
    status_code = 404
    default_detail = 'Not found.'


class MethodNotAllowed(APIException):
    status_code = 405
    default_detail = 'Method "{method}" not allowed.'

    def __init__(self, method, detail=None):
        if detail is not None:
            self.detail = str(detail).format(method=method)
        else:
            self.detail = str(self.default_detail).format(method=method)
        super(MethodNotAllowed, self).__init__()


class NotAcceptable(APIException):
    status_code = 406
    default_detail = 'Could not satisfy the request Accept header.'


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = (
        "The server is currently unable to handle the request, "
        "please try again later")


class NotImplemented:
    status_code = 501
    default_detail = (
        "The server does not support the functionality "
        "required to fulfill the request yet, It is under development")


class DuplicateResource(APIException):
    status_code = 409
    default_detail = (
        "Resource already exists")


class ResourceInMutualExclusionZone(APIException):
    status_code = 409
    default_detail = (
        "Read/Write not allowed on the resource")


class UnProcessableResource(APIException):
    status_code = 422
    default_detail = (
        "Resource is an unprocesseable entity")


class ImproperlyConfigured(APIException):
    status_code = 500
    default_detail = "Improperly Configured"


class ValidationError(APIException):
    status_code = 400
    default_detail = "Bad Request"


class NoContentError(APIException):
    status_code = 204
    default_detail = "No more content to show"
