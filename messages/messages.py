from hclass_common.service_call import get_message_server_template, send_message
from hclass_common.data_types.template_type import (
    A_REQUEST_DECIDE_MATCHING,
    MAN_PROPOSAL_DEACTIVATED, 
    WOMAN_PROPOSAL_DEACTIVATED,
    A_CHAT_OPENED,
    M_DAY_BEFORE_DATE,
    F_DAY_BEFORE_DATE,
    A_HOUR_AND_HALF_BEFORE_DATE,
    F_PUBLISH_FEMALE_PHONE
)
from typing import Dict


def fetch_a_request_message(datejob: str, is_woman: bool = True) -> Dict:
    message_template = get_message_server_template(A_REQUEST_DECIDE_MATCHING)
    message_template['pushTitle'] = message_template['pushTitle'].replace('{dateJob}', datejob)
    message_template['lmsBody'] = message_template['lmsBody'].replace('{dateJob}', datejob)
    if is_woman is False:
        message_template['pushBody'] = message_template['pushBody'].replace('남성', '여성')
    return message_template


def fetch_deactivation_proposal_message(datejob: str, is_woman: bool = True) -> Dict:
    template = WOMAN_PROPOSAL_DEACTIVATED if is_woman else MAN_PROPOSAL_DEACTIVATED
    message_template = get_message_server_template(template)
    message_template['pushBody'] = message_template['pushBody'].replace('{jobName}', datejob)
    message_template['lmsBody'] = message_template['lmsBody'].replace('{jobName}', datejob)
    return message_template


def fetch_a_chat_opened_message(date_nickname: str) -> Dict:
    message_template = get_message_server_template(A_CHAT_OPENED)
    message_template['pushTitle'] = message_template.get('pushTitle').replace('{dateNickname}', date_nickname)
    message_template['lmsBody'] = message_template.get('lmsBody').replace('{dateNickname}', date_nickname)
    return message_template


def fetch_day_before_message(
    is_woman: bool,
    nickname: str,
    date_string: str, selected_title: str, selected_address: str,
    male_job: str = ""
) -> Dict:
    # message.pushTitle = message.pushTitle.replace(/{maleNickname}/gm, maleNickname)
    template_type = F_DAY_BEFORE_DATE if is_woman else M_DAY_BEFORE_DATE 
    message_template = get_message_server_template(template_type)

    message_template['pushBody'] = (
        message_template['pushBody'].replace('{selectedDate}', date_string)
        .replace('{selectedPlaceTitle}', selected_title)
        .replace('{selectedPlaceAddress}', selected_address)
    )
    message_template['lmsBody'] = (
        message_template['lmsBody'].replace('{selectedDate}', date_string)
        .replace('{selectedPlaceTitle}', selected_title)
        .replace('{selectedPlaceAddress}', selected_address)
    )
    if is_woman:
        message_template['pushTitle'] = message_template['pushTitle'].replace('{femaleNickname}', nickname)
        message_template['lmsBody'] = message_template['lmsBody'].replace('{femaleNickname}', nickname)
    else:
        message_template['pushTitle'] = message_template['pushTitle'].replace('{maleNickname}', nickname)
        message_template['lmsBody'] = message_template['lmsBody'].replace("{maleJob}", male_job)
    return message_template


def fetch_one_and_half_messages(
    nickname: str,
    date_string: str, selected_title: str, selected_address: str,
    male_job: str = ""
) -> Dict:
    # message.pushTitle = message.pushTitle.replace(/{maleNickname}/gm, maleNickname)
    message_template = get_message_server_template(A_HOUR_AND_HALF_BEFORE_DATE)

    message_template['pushBody'] = (
        message_template['pushBody'].replace('{selectedDate}', date_string)
        .replace('{selectedPlaceTitle}', selected_title)
        .replace('{selectedPlaceAddress}', selected_address)
    )
    message_template['lmsBody'] = (
        message_template['lmsBody'].replace('{selectedDate}', date_string)
        .replace('{selectedPlaceTitle}', selected_title)
        .replace('{selectedPlaceAddress}', selected_address)
    )
    message_template['pushTitle'] = message_template['pushTitle'].replace('{dateNickname}', nickname)
    message_template['lmsBody'] = message_template['lmsBody'].replace('{dateNickname}', nickname)
    return message_template


def fetch_female_publish_info(date_nickname: str, phone_number: str) -> Dict:
    message_template = get_message_server_template(F_PUBLISH_FEMALE_PHONE)
    message_template['lmsBody'] = message_template.get('lmsBody').replace('{femaleNickname}', date_nickname)
    message_template['lmsBody'] = message_template.get('lmsBody').replace('{femalePhoneNumber}', phone_number)
    return message_template


def send_user_message(message_dict: Dict, user: Dict, is_test: bool) -> Dict:
    fcm_list = user.get("fcm_tokens", [])
    message_dict['receiverPhone'] = user.get("phone_number")
    message_dict['receiverPush'] = fcm_list[-1]
    message_dict['isInstant'] = True
    response = send_message(message_dict, is_test=is_test)
    return response

