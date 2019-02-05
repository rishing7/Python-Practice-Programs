from flask import request
from common import api_exceptions
from flask import make_response
from consumer.utils import get_alert_id_for_Service
from app import app, alert_logger
from scheduler.processor import AlertFactory
from consumer import consumerRouter
from app import celery


@celery.task(name="consumer.views.process_alerts")
def process_alerts(alert_id):
    """
    It acts as a processor for processing service alerts and calling appropriate AlertFactory
    :param alert_id: Unique alert id in the system
    :return: None
    """

    # calling Alert Factory and call specific alert type
    alert_factory = AlertFactory.alert_processor(
        alert_type=app.config['TWILIO_ONCALL_SERVICE']['ALERT_TYPE'],
        alert_id=alert_id,
        account_sid=app.config['TWILIO_ONCALL_SERVICE']['ACCOUNT_SID'],
        account_token=app.config['TWILIO_ONCALL_SERVICE']['ACCOUNT_TOKEN'],
        from_number=app.config['TWILIO_ONCALL_SERVICE']['FROM_NUMBER']
    )
    alert_factory.process_alert()

    return


def alert_handler(service_id):
    """
    Service alert handler creating async tasks for calling third party services
    :param service_id: Unique service Name in the system
    :return: Bool
    """

    try:
        alert_logger.info(
            "Processing Alerts for Service %s" % service_id
        )

        # Generate unique alert ID in a system
        alert_id = get_alert_id_for_Service(service_id)
        alert_logger.info(
            "Alert %s Generated for service %s" % (alert_id, service_id)
        )

        # create celery async tasks
        process_alerts.apply_async(
            args=[str(alert_id)])

        return True
    except Exception as e:
        alert_logger.error(e)
        return False


@consumerRouter.route("/sns", methods=['POST'])
def notif():
    """
    This is the endpoint which act as a subscriber for our AWS SNS service, this endpoint would subscribe
    all the events related to all services registered.

    Endpoint: https://<hostname>:<portNumber>/sns
    Method accepts: [POST]
    Status Codes:
        201: success
        400: Bad request Data

    :return: string
    """
    try:
        alert_logger.info("SNS Endpoint hit")

        # check if request data is received
        if request.data:
            alert_logger.info("SNS Data Received %s" % request.data)
            data = request.get_json()

            # check sns event type
            if data['Type'] == 'Notification':
                # In subject we have alert details such as serviceID
                # TODO: Alert Detail should be part of Message key
                subject = data['Subject']
                service_id = subject.split('ALARM: "')[1].split('-awsroute53')[0]

                # call alert handler for further handling of service alerts
                alert_handler(service_id)
                return make_response(
                    "SNS Request Received")
            else:
                api_exceptions.BadRequestData(
                    "SNS event type is not defined"
                )
        else:
            alert_logger.info("No data is received in SNS notfication")
            return make_response(
                "No data received in SNS Notification"
            )
    except KeyError as e:
        alert_logger.error(str(e))
        raise api_exceptions.BadRequestData(str(e))
