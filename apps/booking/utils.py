import pytz
from django.utils.timezone import localtime

def convert_to_timezone(dt, timezone_str):
    try:
        target_timezone = pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        return dt 
    return localtime(dt, target_timezone)
