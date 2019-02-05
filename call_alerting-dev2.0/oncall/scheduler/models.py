import pytz
from datetime import datetime, timedelta
from common.models import BaseModel
from app import db
from sqlalchemy.orm import validates
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy import and_


class Alert(BaseModel):
    alert_id = db.Column(db.String(128), nullable=False, unique=True)
    is_active = db.Column(db.BOOLEAN, default=True)
    service_id = db.Column(db.INTEGER, db.ForeignKey("service.id"))

    def __repr__(self):
        return "<%s>" % self.alert_id

    @classmethod
    def set_alert(cls, alert_id, is_active=True):
        # HACK: for solving circular error
        from consumer.models import Service

        # get service id from alert name
        service_id = alert_id.split('-')[0].lower()
        service = Service.query.filter_by(service_id=service_id).first()

        # set alert data
        alert = cls(
            alert_id=alert_id, is_active=is_active, service_id=service.id
        )
        db.session.add(alert)
        db.session.commit()

    @classmethod
    def increment_alert_level(cls, alert_id):
        alert = cls.query.filter_by(alert_id=alert_id).first()
        alert.level_id += 1
        db.session.add(alert)
        db.session.commit()

    @classmethod
    def deactivate_alert(cls, alert_id):
        cls.query.filter_by(alert_id=alert_id).update(dict(is_active=False))
        db.session.commit()

    @classmethod
    def get_active_timed_alerts(cls, minutes):
        # get datetime and timezone format time in past minutes
        since_last_half_hour = datetime.now(
            tz=pytz.timezone('Asia/Kolkata')) - timedelta(minutes=minutes)

        # Get all alerts which are active since last 30 minutes
        active_alerts = cls.query.filter(
            and_(
                cls.is_active == True, cls.updated_at >= since_last_half_hour
            )
        ).all()
        return active_alerts


class AlertStatus(BaseModel):
    ALERT_STATUSES = [
        (u'initiated', u'Initiated'),
        (u'passed', u'Passed'),
        (u'missed', u'Missed'),
        (u'accepted', u'Accepted')
    ]
    status = db.Column(ChoiceType(ALERT_STATUSES), unique=True)
    alert_detail = db.relationship("AlertDetail", backref='alert_status', lazy='dynamic')

    @validates('status')
    def validate_status(self, key, status):
        print(key, status)
        return status


class AlertDetail(BaseModel):
    CALL_STATUSES = [
        (u'busy', u'Busy'),
        (u'failed', u'Failed'),
        (u'initiated', u'Initiated'),
        (u'canceled', u'Canceled'),
        (u'completed', u'Completed'),
        (u'no-answer', u'No-Answer')
    ]

    user_level_id = db.Column(db.INTEGER, db.ForeignKey('user_level.id'))
    call_status = db.Column(ChoiceType(CALL_STATUSES), nullable=True)
    response = db.Column(db.String(512), nullable=True)
    call_reference_id = db.Column(db.String(512), nullable=True, unique=True)
    alert_id = db.Column(db.String(128), nullable=False, index=True)
    alert_status_id = db.Column(db.INTEGER, db.ForeignKey("alert_status.id"))

    @classmethod
    def set_alert_details(cls, user_level, call_reference_id, alert_id, alert_status='initiated'):
        alert_Status = AlertStatus.query.filter_by(status=alert_status).first()

        alert_detail = AlertDetail(
            user_level_id=user_level.id, call_reference_id=call_reference_id,
            alert_id=alert_id, alert_status_id=alert_Status.id
        )

        db.session.add(alert_detail)
        db.session.commit()

    @classmethod
    def set_call_alert_status(cls, call_ref, call_status=None, alert_status=None):
        """
        Set Call and Alert Status in different scenarios

        :param call_ref: third party unique call id
        :param call_status: third party call status
        :param alert_status: system generate alert status
        :return:
        """
        # get the call reference object from Alter detail table
        alert_detail = cls.query.filter_by(call_reference_id=call_ref).first()

        # get alert status object if provided
        if alert_status:
            alert_status = AlertStatus.query.filter_by(status=alert_status).first()

        # check if alert status is provided and not call status
        if alert_status and not call_status:
            alert_status = alert_status
            alert_detail.alert_status = alert_status

        elif call_status and not alert_status:
            # Third party(Twilio) provides status of call, our "missed" status of alerts
            # depend on below three negative call statuses, update accordingly
            if call_status in ['busy', 'failed', 'canceled', 'no-answer']:
                alert_detail.alert_status = AlertStatus.query.filter_by(status='missed').first()
            alert_detail.call_status = call_status

        # both call and alert statuses are provided
        else:
            alert_detail.call_status = call_status
            alert_detail.alert_status = alert_status

        db.session.add(alert_detail)
        db.session.commit()

    @classmethod
    def get_user_level(cls, call_ref):
        alert_detail = cls.query.filter_by(call_reference_id=call_ref).first()
        return alert_detail.user_level

    @classmethod
    def check_if_alert_accepted(cls, alert_id):
        # cls.query.join(AlertStatus, AlertStatus.status=='completed').filter(
        #    and_(cls.alert_id == alert_id))
        alert_status = AlertStatus.query.filter_by(status='accepted').first()
        oncall_alert_completed = cls.query.filter(
            and_(cls.alert_id == alert_id, cls.alert_status == alert_status)).all()
        return True if oncall_alert_completed else False

    def __repr__(self):
        return "<%s:%s>" % (self.user_level_id, self.alert_id)
