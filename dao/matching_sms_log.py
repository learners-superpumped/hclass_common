
from typing import TypedDict, Tuple
from .base_dao import BaseDao


class MatchingSmsLogDict(TypedDict):
    matching_id: str
    achat_opened_sent: bool
    gender: str
    m_day_before_date_sent: bool
    f_day_before_date_sent: bool
    hour_and_half_sent: bool
    m_publish_name_sent: bool
    f_publish_female_sent: bool


class MatchingSmsLogDao(BaseDao):

    def fetch_matching_sms_log(
        self,
        matching_id: str
    ) -> Tuple[MatchingSmsLogDict, bool]:
        result = self.client.collection("matching_sms_log").where('matching_id', '==', matching_id).get()
        if result:
            return result[0].to_dict(), result[0].id
        return {
            'achat_opened_sent': False,
            'm_day_before_date_sent': False,
            'f_day_before_date_sent': False,
            'hour_and_half_sent': False,
            'm_publish_name_sent': False,
            'f_publish_female_sent': False,
        }, False

    def insert_dict(
        self,
        data: MatchingSmsLogDict
    ):
        self.client.collection("matching_sms_log").add(data)
        
    def update_dict(
        self,
        dataid: str,
        data: MatchingSmsLogDict
    ):
        self.client.collection("matching_sms_log").document(dataid).update(data)
        