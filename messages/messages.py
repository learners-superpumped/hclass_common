from hclass_common.service_call import get_message_server_template
from hclass_common.data_types.template_type import A_REQUEST_DECIDE_MATCHING
from typing import Dict


def fetch_a_request_message(datejob: str, is_woman: bool = True) -> Dict:
    message_template = get_message_server_template(A_REQUEST_DECIDE_MATCHING)
    message_template['pushTitle'] = message_template['pushTitle'].replace('{dateJob}', datejob)
    message_template['lmsBody'] = message_template['lmsBody'].replace('{dateJob}', datejob)
    if is_woman is False:
        message_template['pushBody'] = message_template['pushBody'].replace('남성', '여성')
    return message_template