from datetime import datetime, timedelta
from app import celery, alert_logger
from scheduler.models import Alert, AlertDetail
from app import alert_cache, app
from notifier.helper import action_after_alert_accepted, \
    action_alert_in_progress, action_alert_level_switch, \
    action_alert_no_response


@celery.task(name='notifier.task.generate')
def generate_email(alert_id):
    alert_cache.delete_alert(alert_id)
    alert_table = Alert.query.filter_by(alert_id=alert_id).first()
    users_list = UserLevel.query.filter_by(service_id=alert_table['service_id'])
    users = Users.query.filter_by([users_list['']])
    # From users_list we will have the user's mail_id and alert_table['response'] will be mentioned in the mail.
    names = []
    emails = []
    for name in users_list['']
    if AlertDetail.check_if_alert_accepted():
        """
            Subject: Issue is resolved
            Email all the users with response.
            
        """
    else:
        """
            Subject: Issue yet to be resolved
            Email
        """



@celery.task(name='notifier.task.monitor_alerts')
def monitor_alerts():
    """
    Monitoring Alerts is a periodic task which finds the active alerts and take action accordingly.
    Runs in few minutes
    :return:
    """
    alert_logger.info(
        "Periodic task Alert Monitoring in action"
    )
    # get last 30 minutes active alerts
    active_alerts = Alert().get_active_timed_alerts(minutes=30)
    for active_alert in active_alerts:
        alert_id = active_alert.alert_id

        # find if active alert is accepted, if so generate mail,delete from cache,Deactivate the alert
        flag_alert_accepted = AlertDetail().check_if_alert_accepted(alert_id)

        if flag_alert_accepted:
            alert_logger.info(
                "Alert %s is accepted " % alert_id +
                "Changing alert state to non active"
            )
            action_after_alert_accepted(alert_id)
            continue

        # get alert cache data i.e alert initiated time and alert counter in each level
        cache_data = alert_cache.get_alert_data(alert_id)
        alert_counter = int(cache_data['counter'])
        last_initiated_time = datetime.strptime(cache_data['initiated_time'], '%Y-%m-%d %H:%M:%S')
        alert_level = int(cache_data['alert_level'])

        # Next Initiated time is when alert is set to trigger in future
        next_initiated_time = last_initiated_time + timedelta(minutes=1)

        # check if initiated_time of alert is
        # --> greater than last five minutes, if so increment the alert counter and set the alert again
        # at the same level of users
        if (next_initiated_time - datetime.now()).total_seconds() < 0 and \
                        alert_counter < app.config['MAX_ONCALL_ALERT_COUNTER']:

            action_alert_in_progress(alert_id, alert_counter, alert_level)

        # check if alert counter is greater than Max_COUNTER value and alert_level is less than MAX_ALERT_LEVEL_ID
        # then set the cache data again i.e alert initiated time, counter to set to one and increment the alert level
        # send the alter again
        elif alert_counter >= app.config['MAX_ONCALL_ALERT_COUNTER'] and \
                        alert_level < app.config['MAX_ALERT_LEVEL_ID']:

            action_alert_level_switch(alert_id, alert_level)

        # Alert has been sent to all level of users,but yet alert is active
        # Delete that alert from the cache and send the mail to all users
        # Deactivate the alert
        elif alert_level >= app.config['MAX_ALERT_LEVEL_ID']:
            action_alert_no_response(alert_id)
        else:
            alert_logger.info(
                "Alert %s is active and in progress" % alert_id
            )
