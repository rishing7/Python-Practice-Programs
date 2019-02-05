SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_ONCALL_ALERT_COUNTER = 2

MAX_ALERT_LEVEL_ID = 3

CELERY_VISIBILITY_TIMEOUT = {'visibility_timeout': 3600}

DEBUG = "<DEBUG TRUE/FALSE>"

REDIS_SERVER = {
    "HOST": "--HOSTNAME--",
    "PORT": "--PORT--",
    "BROKER_DB": '--BROKER DB--',
    "COUNTER_DB": '--COUNTER DB--',
    "TTL": '--TTL--'  # 4 hours
}

DATABASES = {
    "default": {
        "host": "--HOSTNAME--",
        "password": "--PASSWORD--",
        "db_name": "--DB NAME--",
        "port": "--PORT--",
        "user": "--USERNAME--"
    }
}

APP_HOSTNAME = '--APP HOSTNAME'
APP_PORT = '--PORT NUMBER'

TWILIO_ONCALL_SERVICE = {
    "ACCOUNT_SID": "--ACCOUNT ID--",
    "ACCOUNT_TOKEN": "--ACCOUNT TOKEN--",
    "FROM_NUMBER": "--FROM NUMBER--",
    "ALERT_TYPE": "--ALERT TYPE--"
}

TWILIO_STATUS_CALLBACK = {
    "URL": "--CALLBACK URL--",
    "METHOD": "--METHOD--",
    "EVENTS": "--EVENTS NAME--"
}

try:
    from local_settings import *
except ImportError:
    raise Exception("local config not found")

CELERY_BROKER_URL = 'redis://{HOST}:{PORT}/{BROKER_DB}'.format(
    **REDIS_SERVER
)
