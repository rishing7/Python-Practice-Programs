from redis import StrictRedis
from datetime import datetime


class RedisDB(object):
    """
    Base Redis Handler Cache class which interacts with Redis server
    """

    def __init__(self, hostname, port, db, ttl, decode_responses=True):
        self.hostname = hostname
        self.port = port
        self.db = db
        self.decode_responses = decode_responses
        self.ttl = ttl
        self.client = StrictRedis(
            host=self.hostname, port=self.port,
            db=self.db, decode_responses=self.decode_responses
        )

    def set_alert_data(self, alert_id, counter=None, initiated_time=None, alert_level=None):
        # If initiated time is None, set time to datetime.now()
        if not initiated_time:
            initiated_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        # if counter is None, means need to initialise counter
        if not counter:
            counter = 1

        # if alert_level is None, set to first level of alerts
        if not alert_level:
            alert_level = 1

        # set data in redis cache DB
        self.client.hmset(
            alert_id,
            dict(counter=counter, initiated_time=initiated_time, alert_level=alert_level)
        )
        self.client.expire(
            name=alert_id, time=self.ttl)

    def get_alert_data(self, alert_id):
        # get all data fields mapped with given hash
        hdata = self.client.hgetall(alert_id)
        return hdata

    def delete_alert(self, alert_id):
        # Delete a hash from cache
        self.client.delete(alert_id)
