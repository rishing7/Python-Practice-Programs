from app import db
from sqlalchemy.orm import validates
from common.models import BaseModel
from scheduler.models import AlertDetail
from sqlalchemy.exc import InvalidRequestError

LEVEL_IDS = [1, 2, 3]

"""
Lazy parameter determines how the related objects get loaded when querying through relationships.
==> lazy = ‘select’ (or True), lazy = ‘select’ is the default setting. It emits a SELECT statement when 
            loading.Not allow to create a new query on relation tables.
            
==> lazy = ‘dynamic’, When querying with lazy = ‘dynamic’, however, a separate query gets generated for 
            the related object
            
==> lazy = ‘joined’ (or False), lazy = ‘joined’ literally joins the two tables and returns the results in one go.

==> lazy = ‘subquery’, lazy = ‘subquery’ and lazy = ‘joined’ basically do the same thing, except that subquery 
            uses subquery.

"""


class Service(BaseModel):
    service_id = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    userlevel = db.relationship("UserLevel", backref='service', lazy='joined')
    alert = db.relationship("Alert", backref='alert', lazy='dynamic')

    def __repr__(self):
        return "<%s>" % self.name

    @classmethod
    def serviceExists(cls, service_id):
        service = cls.query.filter_by(service_id=service_id).first()
        return True if service else False

    @classmethod
    def update_service_name(cls, service_id, updated_service_id, updated_name):
        cls.query.filter_by(service_id=service_id).update(dict(name=updated_name, service_id=updated_service_id))
        db.session.commit()

    @classmethod
    def get_services(cls, queryDict=None):
        services = []
        try:
            if queryDict:
                services = cls.query.filter_by(**queryDict.to_dict()).all()
            else:
                services = cls.query.all()
            return services
        except InvalidRequestError:
            return services


class Users(BaseModel):
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone_number = db.Column(db.String(16), nullable=False)
    is_active = db.Column(db.BOOLEAN, default=True)
    userlevel = db.relationship("UserLevel", backref='user', lazy='joined')

    @validates('email')
    def validate_email(self, key, email):
        print(key, email)
        return email

    def __repr__(self):
        return "<%s:%s>" % (self.email, self.phone_number)

    @classmethod
    def userExists(cls, email):
        user = cls.query.filter_by(email=email).first()
        return True if user else False

    @classmethod
    def update_user_details(cls, existing_email, updated_fields):
        cls.query.filter_by(email=existing_email).update(updated_fields)
        db.session.commit()

    @classmethod
    def register_user(cls, user, service):
        """
         To register a user, we need to take care of foreign relationships with the table UserLevel
         While adding user in Users table,add a entry in UserLevel
        :param user: user records dictionary such as name,email,phone_number,level_id
        :param service: service object
        :return:
        """

        uobj = cls.query.filter_by(email=user['email']).first()

        # check if user exists, either request came for updating level_id or New user registration
        if not uobj:
            uobj = cls(name=user['name'], email=user['email'], phone_number=user['phone_number'])
            db.session.add(uobj)

            # adding userLevel during transaction of user registration
            ulevel = UserLevel(user=uobj, service=service, level_id=user['level_id'])
            db.session.add(ulevel)

        else:
            # In case if user exists, check for userLevel updation
            ulevel = UserLevel.query.filter_by(user=uobj, service=service, level_id=user['level_id']).first()

            if not ulevel:
                # In case userLevel doesn't exist
                ulevel = UserLevel(user=uobj, service=service, level_id=user['level_id'])
                db.session.add(ulevel)
            else:
                pass

        # commit the transaction in database at one go
        db.session.commit()


class UserLevel(BaseModel):
    service_id = db.Column(db.INTEGER, db.ForeignKey('service.id'))
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'))
    level_id = db.Column(db.INTEGER, default=1, nullable=False)
    call_detail = db.relationship("AlertDetail", backref='user_level', lazy='dynamic')

    def validate_level_id(self, key, level_id):
        if level_id in LEVEL_IDS:
            return level_id
        raise ValueError("Level ID %s is not defined" % level_id)

    @classmethod
    def get_service_users_level(cls, service_id, level_id):
        service = Service.query.filter_by(service_id=service_id).first()
        users_level = cls.query.filter_by(service_id=service.id, level_id=level_id)
        return users_level

    def __repr__(self):
        return "<%s:%s>" % (self.user_id, self.level_id)
