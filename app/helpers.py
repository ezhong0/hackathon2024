import datetime
from .settings import TIMEZONE

def get_datetime():
    return datetime.datetime.now().astimezone(TIMEZONE)
