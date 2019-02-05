from flask import request
from common import api_exceptions
from consumer.models import Service
from consumer.api.schema import ServiceSchema
from http import HTTPStatus
from consumer.api.base import ResourceGetPost, ResourceRetrievePutDelete


class ServiceRegistration(ResourceGetPost):
    """
    Service Registry class consists of POST and GET methods

    For Service Registration API details:
        Endpoint: https://<hostname>:<port>/oncall/service
        METHOD: POST
        Body: {
                "name": "service Name"
                }
        Response: {
                        "response": {
                            "message": "Service is registered successfully",
                            "name": "service_test",
                            "service_id": "service_test",
                            "status_code": 201
                        }
                    }
        Success Status Code: 201

    For Service GET Request:
        Endpoint: https://<hostname>:<port>/oncall/service
        METHOD: GET
        Response:{
                        "response": {
                                "services": [
                                    {
                                        "name": "push_notification_staging",
                                        "service_id": "push_notification_staging"
                                    },
                                    {
                                        "name": "service_test",
                                        "service_id": "service_test"
                                    }
                                ],
                                "status_code": 200
                            }
        }

}
    """
    model = Service
    schema_class = ServiceSchema

    def post(self, *args, **kwargs):
        data, errors = self.schema_class().load(request.json)
        if errors:
            raise api_exceptions.BadRequestData(
                str(errors)
            )
        self.model().create(name=data['name'], service_id=data['service_id'])
        return self.jsonResponse(
            {
                "message": "Service is registered successfully",
                "service_id": data['service_id'], "name": data['name'],
                "status_code": HTTPStatus.CREATED
            },
            HTTPStatus.CREATED
        )

    def get(self, *args, **kwargs):
        response = list()
        services = self.model().get_services(request.args)
        for service in services:
            response.append({"name": service.name, "service_id": service.service_id})
        return self.jsonResponse(
            {"services": response, "status_code": HTTPStatus.OK}
        )


class EditService(ResourceRetrievePutDelete):
    """
    Edit and Retrieve Service class
    For Specific Service details:
        Endpoint: https://<hostname>:<port>/oncall/service/<service_id>
        METHOD: GET
        Response:  {
                    "response": {
                        "name": "push_notification_staging",
                        "service_id": "push_notification_staging",
                        "status_code": 200
    }
    For Specific Service details:
        Endpoint: https://<hostname>:<port>/oncall/service/<service_id>
        METHOD: PUT
        Body:{
                "name": <Updated new Service Name>
        }
        Response:  {
                    "response": {
                        "message": "Service is sucessfully updated",
                        "name": "servicetest",
                        "service_id": "servicetest",
                        "status_code": 202
                    }
                }
    """
    model = Service
    schema_class = ServiceSchema

    def get(self, service_id):
        service = self.model.query.filter_by(service_id=service_id).first()
        if service:
            return self.jsonResponse(
                {
                    "service_id": service.service_id,
                    "name": service.name,
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

    def put(self, service_id):
        if self.model.serviceExists(service_id):
            data, errors = self.schema_class().load(request.json)
            if errors:
                raise api_exceptions.BadRequestData(
                    str(errors)
                )
            self.model.update_service_name(service_id=service_id, updated_name=data['name'],
                                           updated_service_id=data['service_id'])
            return self.jsonResponse(
                {
                    "message": "Service is sucessfully updated",
                    "service_id": data['service_id'], "name": data['name'],
                    "status_code": HTTPStatus.ACCEPTED
                },
                HTTPStatus.ACCEPTED
            )
        else:
            return self.jsonResponse(
                {
                    "error": "Service doesn't exist",
                    "status_code": HTTPStatus.BAD_REQUEST
                },
                HTTPStatus.BAD_REQUEST
            )
