from datetime import datetime as dt, timedelta
from pythoncommon.timeutils import get_now_time_dt


def check_achat_open_time(selected_appointment: dt):
    now_time = get_now_time_dt()
    delta = selected_appointment - now_time
    if delta > timedelta(hours=48) and delta < timedelta(hours=48, minutes=30):
        return True
    return False
  

def check_date_before_date(selected_appointment: dt):
    now_time = get_now_time_dt()
    delta = selected_appointment - now_time
    if delta >= timedelta(hours=24) and delta < timedelta(hours=24, minutes=30):
        return True
    return False
    

def check_one_and_half_hour(selected_appointment: dt):
    now_time = get_now_time_dt()
    delta = selected_appointment - now_time
    if delta >= timedelta(hours=1, minutes=20) and delta < timedelta(hours=1, minutes=40):
        return True
    return False


def check_publish_time(selected_appointment: dt):
    now_time = get_now_time_dt()
    delta = selected_appointment - now_time
    if delta >= timedelta(minutes=10) and delta < timedelta(minutes=20):
        return True
    return False