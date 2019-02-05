import time
import uuid


def generate_random_string(string_length=6):
    """
    Generating Random string of given length
    :param string_length: integer
    :return:
    """
    random_string = str(uuid.uuid4())
    random_string = random_string.upper()
    random_string = random_string.replace("-", "")
    return random_string[:string_length]


def get_alert_id_for_Service(service_id):
    """
    Generating Unique alert ID in system
    Format: <service_id(upper case)> - <current epoch timestamp> - <random 6 alphaNumeric Letters>
    :param service_id: ID of service
    :return: alert ID
    """
    service_id = service_id.upper()
    random_string = generate_random_string(string_length=6)
    return "-".join((service_id, str(int(time.time())), random_string))
