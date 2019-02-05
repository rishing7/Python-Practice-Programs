from flask import (
    request,
    url_for
)
from twilio.twiml.voice_response import VoiceResponse
from scheduler.models import AlertDetail, Alert
from scheduler.helper import twiml
from scheduler import schedulerRouter
from app import app

IVR_VOICE = 'alice'
IVR_LANGUAGE = 'en-IN'


@schedulerRouter.route('/ivr/initiate', methods=['POST'])
def initiate():
    """
    Initiation function in IVR Flow
    :return:
    """
    response = VoiceResponse()
    user_level = AlertDetail.get_user_level(call_ref=request.form['CallSid'])
    with response.gather(
            num_digits=1, action="%s/ivr/menu" % app.config['APP_HOSTNAME'], method="POST", timeout=10
    ) as g:
        g.say(
            message="Hi {user},".format(user=user_level.user.name) +
                    "{service_name} service is either down or behaving unexpectedly,".format(
                        service_name=" ".join(user_level.service.service_id.split("_"))) +
                    "For Accepting the issue then Press 1," +
                    "Passing on to other team member then Press 2," +
                    "Want to Listen Again then Press 3",

            loop=1, language=IVR_LANGUAGE, voice=IVR_VOICE
        )
    return twiml(response)


@schedulerRouter.route('/ivr/menu', methods=['POST'])
def menu():
    """
    Function to hold the Menu for IVR
    :return:
    """
    selected_option = request.form['Digits']
    option_actions = {'1': accept_issue,
                      '2': pass_on_issue,
                      '3': redirect_initiate}

    if selected_option in option_actions:
        response = VoiceResponse()
        option_actions[selected_option](response)
        return twiml(response)
    return incorrect_response()


@schedulerRouter.route('/ivr/status', methods=['POST'])
def update_call_status():
    """
    Twilio updating the status using this endpoint.
    :return:
    """
    AlertDetail().set_call_alert_status(call_ref=request.form['CallSid'], call_status=request.form['CallStatus'])
    return twiml("Call Status updated")


def accept_issue(response):
    """
    Action to take place once alert hash been accepted by user
    :param response:
    :return:
    """
    response.say(
        "Thank you for your response",
        language=IVR_LANGUAGE, voice=IVR_VOICE
    )
    response.hangup()
    AlertDetail().set_call_alert_status(
        call_ref=request.form['CallSid'], alert_status='accepted'
    )
    return response


def pass_on_issue(response):
    """
    Action to take place once user passed on the alert to other team members
    :param response:
    :return:
    """
    response.say(
        "Thank you for your response",
        language=IVR_LANGUAGE, voice=IVR_VOICE
    )
    response.hangup()
    AlertDetail().set_call_alert_status(
        call_ref=request.form['CallSid'], alert_status='passed'
    )
    return response


def incorrect_response():
    """
    Action to take in case incorrect response received from user
    :return:
    """
    response = VoiceResponse()
    response.say(
        "The response entered is not correct. Let's start over.",
        voice=IVR_VOICE, language=IVR_LANGUAGE
    )
    response.redirect(url_for('scheduler.initiate'))

    return twiml(response)


def redirect_initiate(response):
    response.redirect(url_for('scheduler.initiate'))
    return response
