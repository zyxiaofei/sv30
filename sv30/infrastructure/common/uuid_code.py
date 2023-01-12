import uuid
import random


def get_uuid():
    data = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random())))
    return data
