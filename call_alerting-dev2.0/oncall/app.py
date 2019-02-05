import os
import logging
import logging.handlers
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_restful import Api
from celery.schedules import crontab
from common.redis import RedisDB

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'logs')

# SET UP LOGGING
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info').upper()

# Common formatter
formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s", "%Y-%m-%d %H:%M:%S")

# Handler for stdout
handler_stdout = logging.StreamHandler()
handler_stdout.setLevel(LOG_LEVEL)
handler_stdout.setFormatter(formatter)


def initialise_app(configfile):
    """
    Initialise and configure the main flask App.
    """
    app = Flask(__name__)
    api = Api(app)
    app.config.from_pyfile(configfile)
    return app, api


def initialise_db_binds(app_instance):
    """
    Initialise the database instance
    """
    db_details = app_instance.config["DATABASES"]
    sql_binds = dict()
    for db_tag, db_detail in db_details.items():
        db_url = 'postgresql://{user}:{password}@{host}:{port}/{db_name}' \
            .format(user=db_detail['user'],
                    password=db_detail['password'],
                    host=db_detail['host'],
                    port=db_detail['port'],
                    db_name=db_detail['db_name'])
        sql_binds[db_tag] = db_url
    app_instance.config['SQLALCHEMY_BINDS'] = sql_binds
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = sql_binds['default']
    return


def initialise_logger():
    LOG_FILENAME = os.path.join(LOG_PATH, 'alert.log')
    # Set up a specific logger with our desired output level
    alert_logger = logging.getLogger('AlertLogger')
    alert_logger.setLevel(LOG_LEVEL)
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)
    alert_logger.addHandler(handler)
    alert_logger.addHandler(handler_stdout)
    return alert_logger


def initialise_celery(app_instance):
    """
    Initialise and configure celery instance
    """
    celery = Celery(
        app_instance.name,
        broker=app_instance.config['CELERY_BROKER_URL'])
    celery.conf.update(
        CELERY_BROKER_URL=app_instance.config['CELERY_BROKER_URL'],
        BROKER_TRANSPORT_OPTIONS=app_instance.config['CELERY_VISIBILITY_TIMEOUT'],
        CELERY_IMPORTS=('consumer.views', 'notifier.task'),
        CELERYBEAT_SCHEDULE={
            # Executes every minute
            'monitor_alerts-every-minute': {
                'task': 'notifier.task.monitor_alerts',
                'schedule': crontab(minute="*")
            }
        }
    )
    return celery


def initialise_alert_cache(app_instance):
    """
    Initialise redis cache db
    """
    redis_details = app_instance.config['REDIS_SERVER']
    redis = RedisDB(
        hostname=redis_details['HOST'],
        port=redis_details['PORT'],
        db=redis_details['COUNTER_DB'],
        ttl=redis_details['TTL']
    )
    return redis


alert_logger = initialise_logger()
app, api = initialise_app("settings.py")
celery = initialise_celery(app)
initialise_db_binds(app)
db = SQLAlchemy(app)
alert_cache = initialise_alert_cache(app)