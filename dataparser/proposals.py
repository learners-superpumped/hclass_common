from typing import List, Dict, Optional
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


def fetch_inactive_proposal_list(proposal_list: List[Dict]) -> List[Dict]:
    new_proposal_list = [x for x in proposal_list if x.get('is_passed') is False and x.get("is_matched") is False]
    return new_proposal_list

def fetch_oldest_proposal(proposal_list: List[Dict]) -> Dict:
    oldest_create_time = sorted(proposal_list, key=lambda x: x.get('created_at'), reverse=False)[0]
    return oldest_create_time

def fetch_newest_proposal(proposal_list: List[Dict]) -> Dict:
    newest_create_time = sorted(proposal_list, key=lambda x: x.get('created_at'), reverse=True)[0]
    return newest_create_time

def calculate_last_action_time(proposal_list: List[Dict]) -> DatetimeWithNanoseconds:
    last_passed_time = None
    last_matched_time = None
    for proposal_data in proposal_list:
        if proposal_data.get('is_passed'):
            if last_passed_time is None and proposal_data.get('passed_at'):
                last_passed_time = proposal_data.get('passed_at')
            if last_passed_time and proposal_data.get('passed_at') and proposal_data.get('passed_at') > last_passed_time:
                last_passed_time = proposal_data.get("passed_at")
        if proposal_data.get('is_matched'):
            if last_matched_time is None and proposal_data.get('matched_at'):
                last_matched_time = proposal_data.get('matched_at')
            if last_matched_time and proposal_data.get('matched_at') and proposal_data.get('matched_at') > last_matched_time:
                last_matched_time = proposal_data.get('matched_at')

    action_time = [last_passed_time, last_matched_time]
    action_time = [x for x in action_time if x is not None]
    if not action_time:
        oldest_create_time = sorted(proposal_list, key=lambda x: x.get('created_at'), reverse=False)
        return oldest_create_time[0].get('created_at')
    return max(action_time)

def last_create_time(proposal_list: List[Dict]) -> Optional[DatetimeWithNanoseconds]:
    latest_create_time = sorted(proposal_list, key=lambda x: x.get('created_at'), reverse=True)[0]
    return latest_create_time