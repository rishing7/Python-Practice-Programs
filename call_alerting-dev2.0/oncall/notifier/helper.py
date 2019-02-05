from app import alert_cache
from scheduler.models import Alert
from consumer.views import process_alerts


def generate_email(alert_id):
    pass


def action_after_alert_accepted(alert_id):
    """
    Different Actions to take place, once alert in accepted state
    :param alert_id:
    :return:
    """
    generate_email(alert_id)
    alert_cache.delete_alert(alert_id)
    Alert().deactivate_alert(alert_id)


def action_alert_in_progress(alert_id, alert_counter, alert_level):
    """
    Actions take place when alert in progress state
    :param alert_id:
    :param alert_counter:
    :param alert_level:
    :return:
    """
    alert_cache.set_alert_data(
        alert_id,
        counter=alert_counter + 1, alert_level=alert_level)
    # create celery async tasks
    process_alerts.apply_async(
        args=[str(alert_id)])


def action_alert_level_switch(alert_id, alert_level):
    """
    Action take place when alert switches the level
    :param alert_id:
    :param alert_level:
    :return:
    """
    alert_cache.set_alert_data(
        alert_id, alert_level=alert_level + 1)

    # create celery async tasks
    process_alerts.apply_async(
        args=[str(alert_id)])


def action_alert_no_response(alert_id):
    """
    Action take place when No response got from Users from different Level
    :param alert_id:
    :return:
    """
    alert_cache.delete_alert(alert_id)
    Alert().deactivate_alert(alert_id)
    # generate_mail(alert_id)
