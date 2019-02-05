from flask import Response


def twiml(resp):
    """
    Make Twilio HTTP Response
    :param resp:
    :return:
    """
    resp = Response(str(resp))
    return resp
