from typing import Dict, List
from .base_dao import BaseDao
from firebase_admin import firestore
from hclass_common.utils.func_utils import retries
import pytz
from datetime import datetime as dt


class ProposalDao(BaseDao):

    def fetch_proposals(
        self,
        uid: str,
    ) -> List[Dict]:
        data_list = self.client.collection("proposals").where("uid", '==', uid).get()
        new_data_list = []
        for x in data_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            new_data_list.append(datadict)
        return new_data_list

    def fetch_daily_man_count_map(
        self,
    ) -> Dict[str, int]:
        tzinfo = pytz.timezone("Asia/Seoul")
        dtdata = dt(year=dt.now().year, month=dt.now().month, day=dt.now().day)
        todaytime = dtdata.replace(tzinfo=tzinfo)
        data_list = self.client.collection("proposals").where("gender", '==', "여성").where("created_at", ">", todaytime).get()
        total_map = {}
        for x in data_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            partner_uid = datadict.get("partner_uid")
            if not total_map.get(partner_uid):
                total_map[partner_uid] = 1
            else:
                total_map[partner_uid] += 1
        return total_map

    def fetch_today_proposals(
        self,
    ) -> List[Dict]:
        data_list = self.client.collection("proposals").where('is_matched', '==', False).where("is_passed", '==', False).get()
        new_data_list = []
        for x in data_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            new_data_list.append(datadict)
        return new_data_list

    def deactivate_proposals(
        self,
        proposal_id
    ) -> List[Dict]:
        current_timestamp = firestore.SERVER_TIMESTAMP
        self.client.collection("proposals").document(proposal_id).update({
            'is_deactivated': True,
            'deactivated_at': current_timestamp
        })

    @retries(4, 4)
    def fetch_recent_proposal(
        self,
        man_uid: str,
        woman_uid: str, 
    ) -> Dict:

        data_list = self.client.collection("proposals").where("uid", '==', man_uid).where('partner_uid', '==', woman_uid).get()
        new_data_list = []
        for x in data_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            new_data_list.append(datadict)
        data = sorted(new_data_list, key=lambda x: x.get('created_at'), reverse=True)[0]
        return data

    def delete_related_proposals(
        self, 
        uid: str, 
    ):
        proposal_list = self.client.collection("proposals").where('uid', '==', uid).get()
        for proposal_data in proposal_list:
            self.client.collection("proposals").document(proposal_data.id).delete()
        partner_proposal_list = self.client.collection("proposals").where('partner_uid', '==', uid).get()
        for proposal_data in partner_proposal_list:
            self.client.collection("proposals").document(proposal_data.id).delete()

    @retries(5)
    def match_proposal(
        self, 
        proposal_id: str, 
    ):
        self.client.collection("proposals").document(proposal_id).update({
            'is_matched': True,
            "matched_at": firestore.SERVER_TIMESTAMP
        })

    def create_proposal(
        self, 
        woman_user: Dict,
        partner_user: Dict,
        partner_user_evaluation: Dict
    ):
        _, proposal_ref = self.client.collection("proposals").add({
            "uid": woman_user.get('uid'),
            "gender": "여성",
            "partner": {
                "hclass_level": partner_user_evaluation.get("hclass_level"),
                "concierge_oneline": partner_user_evaluation.get("concierge_oneline"),
                "concierge_comment": partner_user_evaluation.get("concierge_comment"),
                "short_introduction": partner_user_evaluation.get("short_introduction"),
                "school": partner_user.get("school"),
                "religion": partner_user.get("religion"),
                "region": partner_user.get('region'),
                "profile_type": partner_user.get("profile_type"),
                "profile_image_url": partner_user.get("profile_image_url"),
                "preferred_type_for_female": partner_user.get("preferred_type_for_female"),
                "phone_number": partner_user.get("phone_number"),
                "nickname": partner_user.get('nickname'),
                "namecard_image_url": partner_user.get('namecard_image_url'),
                "mbti": partner_user.get("mbti"),
                "looking_for": partner_user.get('looking_for'),
                "look_type": partner_user.get("look_type"),
                "long_introduction": partner_user.get("long_introduction"),
                "job_name": partner_user.get("job_name"),
                "job_category": partner_user.get("job_category"),
                "inflow": partner_user.get("inflow"),
                "height": partner_user.get("height"),
                "gender": partner_user.get("gender"),
                "education": partner_user.get("education"),
                "drink": partner_user.get("drink"),
                "divorce": partner_user.get("divorce"),
                "created_at": partner_user.get("created_at"),
                "body_shape": partner_user.get("body_shape"),
                "birthday": partner_user.get("birthday"),
                "badges": partner_user.get("badges", []),
                "after_match": partner_user.get('after_match'),
                "additional_images_url": partner_user.get("additional_images_url", []),
            },
            "created_at": firestore.SERVER_TIMESTAMP,
            "created": firestore.SERVER_TIMESTAMP,
            "is_read": False,
            "is_matched": False,
            "partner_uid": partner_user.get('uid'),
            "is_passed": False,
        })
        return proposal_ref