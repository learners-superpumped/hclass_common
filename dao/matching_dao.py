from typing import Dict, Tuple
from .base_dao import BaseDao
from firebase_admin import firestore
from datetime import datetime as dt
from utils.timeutils import set_hour_24, fetch_appointments_list
from utils.func_utils import retries


class MatchingDao(BaseDao):

    def delete_related_matchings(
        self, 
        uid: str, 
    ):
        proposal_list = self.client.collection("matchings").where('uid', '==', uid).get()
        for proposal_data in proposal_list:
            self.client.collection("matchings").document(proposal_data.id).delete()
        partner_proposal_list = self.client.collection("matchings").where('partner_uid', '==', uid).get()
        for proposal_data in partner_proposal_list:
            self.client.collection("matchings").document(proposal_data.id).delete()

        matching_complete_list = self.client.collection("matching_completes").where('male_user_uid', '==', uid).get()
        for matching_complete in matching_complete_list:
            self.client.collection("matching_completes").document(matching_complete.id).delete()
        matching_complete_list = self.client.collection("matching_completes").where('female_user_uid', '==', uid).get()
        for matching_complete in matching_complete_list:
            self.client.collection("matching_completes").document(matching_complete.id).delete()

    @retries(4, 4)
    def fetch_recent_woman_matching(
        self,
        man_uid: str,
        woman_uid: str, 
    ) -> Dict:
        data_list = self.client.collection("matchings").where("uid", '==', woman_uid).where('partner_uid', '==', man_uid).get()
        new_data_list = []
        for x in data_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            new_data_list.append(datadict)
        data = sorted(new_data_list, key=lambda x: x.get('created_at'), reverse=True)[0]
        return data
    
    @retries(4, 5)
    def fetch_recent_man_matching(
        self,
        man_uid: str,
        woman_uid: str, 
    ) -> Dict:
        data_list = self.client.collection("matchings").where("uid", '==', man_uid).where('partner_uid', '==', woman_uid).get()
        new_data_list = []
        for x in data_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            new_data_list.append(datadict)
        data = sorted(new_data_list, key=lambda x: x.get('created_at'), reverse=True)[0]
        return data

    def activate_matching_data(
        self,
        woman_matching_id: str,
        man_matching_id: str,
    ) -> Dict:

        self.client.collection('matchings').document(woman_matching_id).update(
            {
                "is_active": True, 
                "women_status_ready_at": firestore.SERVER_TIMESTAMP,
                "confirm_time_limit": set_hour_24()

            }
        )
        self.client.collection('matchings').document(man_matching_id).update(
            {
                "is_active": True, 
                "women_status_ready_at": firestore.SERVER_TIMESTAMP,
                "status": "not_ready"
            }
        )

    def insert_matching_data(self, man_user, woman_user) -> Tuple[Dict, Dict]:
        _, man_matching_ref = self.client.collection('matchings').add({
            "created_at": firestore.SERVER_TIMESTAMP,
            "is_active": True,
            "status": 'not_ready',
            "gender": '남성',
            "uid": man_user.get("uid"),
            "my_region": man_user.get("region"),
            "partner_uid": woman_user.get("uid"),
            "partner_region": woman_user.get("region"),
            "partner_profile_image_url": woman_user.get("partner_profile_image_url"),
            "partner_nickname": woman_user.get("nickname"),
            "partner_job_category": woman_user.get("partner_job_category"),
        })
        _, woman_matching_ref = self.client.collection('matchings').add({
            "created_at": firestore.SERVER_TIMESTAMP,
            "is_active": False,
            "status": 'default',
            "gender": '여성',
            "uid": woman_user.get("uid"),
            "my_region": woman_user.get("region"),
            "partner_uid": man_user.get("uid"),
            "partner_region": man_user.get("region"),
            "partner_profile_image_url": man_user.get("partner_profile_image_url"),
            "partner_nickname": man_user.get("nickname"),
            "partner_job_category": man_user.get("partner_job_category"),
        })
        return man_matching_ref, woman_matching_ref

    def confirm_female_time_place(
        self,
        woman_matching_id: str,
        preferred_region: str = '한남동',
        preferred_place_type: str = '레스토랑',
        manner_comment: str="반갑습닏. 저는 커피도 식사도 좋아요 :-)",
    ) -> Dict:
        timelist = fetch_appointments_list()
        confirm_time_limit = set_hour_24()
        self.client.collection('matchings').document(woman_matching_id).update(
            {
                "women_status_ready_at": firestore.SERVER_TIMESTAMP,
                "confirm_time_limit": set_hour_24(1),
                "preferred_region": preferred_region,
                "preferred_place_type": preferred_place_type,
                "manner_comment": manner_comment,
                "appointments": timelist,
                "female_confirmed_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP
            }
        )
        