from marshmallow import Schema, fields, post_load, ValidationError, validates
from consumer.models import Service, LEVEL_IDS


class ServiceSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Service Name is required'})

    def generate_service_id(self, data):
        tobeReplaces = ["-", " "]
        name = data['name'].lower()
        for repl in tobeReplaces:
            name.replace(repl, "_")
        return name

    @post_load
    def check_service_id_unique(self, data):
        service_id = self.generate_service_id(data)
        serviceExists = Service.query.filter_by(
            service_id=service_id).first()
        if serviceExists:
            raise ValidationError("Service Name is already taken.")
        data['service_id'] = service_id
        return data


class UserSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'User Name is required'})
    email = fields.Email(required=True, error_messages={'invalid': 'Not a valid email address.'})
    phone_number = fields.Str(required=True)
    level_id = fields.Int(required=True, error_messages={'required': 'User Level Id is required'})

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        print(phone_number)
        return phone_number

    @validates('level_id')
    def validate_level_id(self, level_id):
        if level_id not in LEVEL_IDS:
            raise ValidationError("Level ID validation error, should be in [1,2,3]")
        return level_id


class UserServiceSchema(Schema):
    service_id = fields.Str(required=True, error_messages={'required': 'Service ID is required'})
    users = fields.Nested(UserSchema, many=True)

    @validates('service_id')
    def validate_service_id(self, service_id):
        service = Service.query.filter_by(service_id=service_id).first()
        if not service:
            raise ValidationError("Service ID doesn't exist")
        return service_id
