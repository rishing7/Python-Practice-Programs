from app import alert_logger, app
from twilio.rest import Client
from scheduler.models import Alert, AlertDetail
from consumer.models import UserLevel
from app import alert_cache


class AlertFactory(object):
    """
    Factory class for returning specific alert type
    """

    @staticmethod
    def alert_processor(alert_type, alert_id, account_sid, account_token, from_number=None):
        """
        Processor return the instance of alert depending on alert type string

        :param alert_type: alert type
        :param alert_id: unique alert ID
        :param account_sid: Third party auth sid
        :param account_token: third party auth token
        :param from_number: Number to be visible
        :return: alert type object
        """
        if alert_type == 'oncall':
            return OncallAlertProcessor(
                alert_type, alert_id,
                account_sid, account_token,
                from_number
            )
        else:
            alert_logger.info("No alert processor is defined for alert type %s" % alert_type)
            return None


class AlertProcessor(object):
    """
    Base class for every alert type processor
    """

    def __init__(self, alert_id, account_sid, account_token):
        self.alert_id = alert_id
        self.account_sid = account_sid
        self.account_token = account_token
        self.service_id = alert_id.split("-")[0].lower()


class OncallAlertProcessor(AlertProcessor):
    """
    Oncall Processor called the user in case alerts are generated
    """

    def __init__(self, alert_type, alert_id, account_sid, account_token, from_number):

        # Set __init__ method of Base class parameters
        super(OncallAlertProcessor, self).__init__(alert_id, account_sid, account_token)

        # alert type, this case is oncall
        self.alert_type = alert_type

        # In sec, call timeout for ringing phone
        self.call_ringing_timeout = '60'

        # third party phone number for display
        self.from_number = from_number

        # Twilio status callback methods
        self.status_callback_url = app.config['TWILIO_STATUS_CALLBACK']['URL']
        self.status_callback_method = app.config['TWILIO_STATUS_CALLBACK']['METHOD']
        self.status_callback_events = app.config['TWILIO_STATUS_CALLBACK']['EVENTS']

        self.callback_url = "%s/ivr/initiate" % app.config['APP_HOSTNAME']

        # call third party client, this case is for Twilio
        self.client = Client(
            self.account_sid, self.account_token)

        # set alert in db
        self.set_alert_db()

    def set_alert_db(self):
        """
        Set alert level in database,
        In case No alert found in db, means first time alert generated -->> then set level_id as 1
        else it would remains same
        :return:
        """

        # Get alert object from db
        alert = Alert.query.filter_by(alert_id=self.alert_id).first()

        # check if alert exists and set accordingly
        if not alert:
            Alert().set_alert(alert_id=self.alert_id)

            # counter used for maintaining alert sent counts at each level
            alert_cache.set_alert_data(
                self.alert_id
            )

    def process_alert(self):
        """
        This function helps in processing the alert
        :return:
        """
        # Get current alert level for getting specific users
        current_alert_level = alert_cache.get_alert_data(self.alert_id)['alert_level']

        # Get all user level of service set in for alert generation
        users_level = UserLevel().get_service_users_level(self.service_id, current_alert_level)

        for user_level in users_level:
            alert_logger.info(
                "Call Detail To Number %s from Number %s" % (user_level.user.phone_number, self.from_number))
            self.generate_alert(user_level)

    def generate_alert(self, user_level):
        """
        This function would generate alerts via calling third party APIs(Twilio)
        :param user_level:
        :return:
        """
        call = self.client.calls.create(
            url=self.callback_url,
            to=user_level.user.phone_number,
            from_=self.from_number,
            timeout=self.call_ringing_timeout,
            status_callback=self.status_callback_url,
            status_callback_event=self.status_callback_events,
            status_callback_method=self.status_callback_method
        )
        # set alert details in db
        AlertDetail().set_alert_details(
            user_level=user_level,
            call_reference_id=call.sid,
            alert_id=self.alert_id
        )
