from consumer.api.base import ResourceGetPost, ResourceRetrievePutDelete
from consumer.models import Users, UserLevel, Service
from flask import request
from consumer.api.schema import UserServiceSchema, UserSchema
from common import api_exceptions
from http import HTTPStatus


class UserRegistration(ResourceGetPost):
    """
    User Registration
    Endpoint: https://<hostname>:<port>/oncall/user
        METHOD: POST
        Body: {
                "service_id": "push_notification_staging",
                "users":[
                    {
                        "name": "Bharat Gera 3",
                        "email": "bharat.gera3@ril.com",
                        "phone_number": "+919326716393",
                        "level_id": 3
                    }
                    ]
            }
        Response:
            {
                    "response": {
                        "message": "Users are registered successfully with level ids",
                        "status_code": 201
                    }
    }

    Endpoint: http://localhost:8000/oncall/user?service_id=<service_id>
        METHOD: GET
        Response:
                        {
                        "response": {
                            "status_code": 200,
                            "users": [
                                {
                                    "email": "bharat.gera@ril.com",
                                    "name": "Bharat Gera",
                                    "phone_number": "+919326716393",
                                    "user_level": 1
                                },
                                {
                                    "email": "bharat.gera2@ril.com",
                                    "name": "Bharat Gera 2",
                                    "phone_number": "+919326716393",
                                    "user_level": 2
                                }
                            ]
                        }
                    }

    """
    model = Users
    schema_class = UserServiceSchema

    def post(self, *args, **kwargs):
        """
        POST USER Request
        """
        data, errors = self.schema_class().load(request.json)
        if errors:
            raise api_exceptions.BadRequestData(
                errors
            )
        service = Service.query.filter_by(service_id=data['service_id']).first()
        for user in data['users']:
            self.model.register_user(user, service)
        return self.jsonResponse(
            {
                "message": "Users are registered successfully with level ids",
                "status_code": HTTPStatus.CREATED
            },
            HTTPStatus.CREATED
        )

    def get(self, *args, **kwargs):
        user_details = []
        service_id = request.args.get('service_id')
        service = Service.query.filter_by(service_id=service_id).first()
        if not service:
            return self.jsonResponse(
                {
                    "error": "Service doesn't exist",
                    "status_code": HTTPStatus.NOT_FOUND
                }
            )
        userlevels = service.userlevel
        for userlevel in userlevels:
            user = userlevel.user
            user_details.append({"name": user.name, "email": user.email, "phone_number": user.phone_number,
                                 "user_level": userlevel.level_id})
        return self.jsonResponse(
            {
                "users": user_details,
                "status_code": HTTPStatus.OK
            },
            HTTPStatus.OK
        )


class EditUser(ResourceRetrievePutDelete):
    """
    Edit and Retrieve User using email address(unique in system)
    For Specific User details:
        Endpoint: https://<hostname>:<port>/oncall/user/<email_id>
        METHOD: GET
        Response:  {
                        "response": {
                            "email": "bharat.gera@ril.com",
                            "name": "Bharat Gera",
                            "phone_number": "+919326716393",
                            "status_code": 200
                        }
                    }
    For Update User details:
        Endpoint: https://<hostname>:<port>/oncall/user/<emailID>
        Method: PUT
        Body: {
                    "phone_number": "+9190922232422"
            }
        Response:{
                "response": {
                    "message": "User is sucessfully updated",
                    "status_code": 202
                    }

            }
    """
    model = Users
    schema_class = UserSchema

    def get(self, email):

        user = self.model.query.filter_by(email=email).first()
        if user:
            return self.jsonResponse(
                {
                    "name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "status_code": HTTPStatus.OK
                },
                HTTPStatus.OK
            )
        else:
            return self.jsonResponse(
                {
                    "error": "service doesn't exist",
                    "status_code": HTTPStatus.BAD_REQUEST
                },
                HTTPStatus.BAD_REQUEST
            )

    def put(self, email):
        if self.model.userExists(email):
            data, errors = self.schema_class(partial=True).load(request.json)
            if errors or not data:
                raise api_exceptions.BadRequestData(
                    errors
                )

            self.model.update_user_details(existing_email=email, updated_fields=data)
            return self.jsonResponse(
                {
                    "message": "User is successfully updated",
                    "status_code": HTTPStatus.ACCEPTED
                },
                HTTPStatus.ACCEPTED
            )
        else:
            return self.jsonResponse(
                {
                    "error": "User doesn't exist",
                    "status_code": HTTPStatus.BAD_REQUEST
                },
                HTTPStatus.BAD_REQUEST
            )


class DeleteUser(ResourceRetrievePutDelete):
    def delete(self, email, service_id):
        pass
