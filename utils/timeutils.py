from typing import List
from datetime import datetime as dt, timedelta, time
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from firebase_admin import firestore
import pytz



def convert_time(data: DatetimeWithNanoseconds) -> dt:
    try:
        return dt.fromtimestamp(data.timestamp())
    except Exception:
        return data


def convert_kst_time(data: DatetimeWithNanoseconds) -> dt:
    try:
        tzinfo = pytz.timezone("Asia/Seoul") 
        return dt.fromtimestamp(data.timestamp()).replace(tzinfo=tzinfo)
    except Exception:
        return data

def convert_string_to_time(data: str) -> dt:
    try:
        tzinfo = pytz.timezone("Asia/Seoul") 
        dtdata =  dt.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
        return dtdata.replace(tzinfo=tzinfo)
    except Exception:
        return data


def set_hour_24(datediff: int = 0) -> dt:
    tzinfo = pytz.timezone("Asia/Seoul") 
    current_time = dt.now(tzinfo)
    target_day = current_time + timedelta(days=datediff) 
    midnight_aware = tzinfo.localize(
        dt.combine(target_day, time(0, 0, 0, 0)), is_dst=None
    )
    return midnight_aware



def fetch_appointments_list() -> List[dt]:
    tzinfo = pytz.timezone("Asia/Seoul") 
    current_time = dt.now(tzinfo)
    time_list = []
    for i in range(1, 5):
        target_day = current_time + timedelta(days=i) 
        midnight_aware = tzinfo.localize(
            dt.combine(target_day, time(18, 0, 0, 0)), is_dst=None
        )
        time_list.append(midnight_aware)
    return time_list
