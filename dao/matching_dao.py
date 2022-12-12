from typing import Dict, Tuple, Optional
from .base_dao import BaseDao
from firebase_admin import firestore
from hclass_common.utils.timeutils import set_hour_24, fetch_appointments_list
from hclass_common.utils.func_utils import retries

DEFAULT_SELECTED_PLACE = {
    'roadAddress': '서울특별시 영등포구 국제금융로8길 31 K-Tower 1층 105호, 106호',
    'link': 'http://www.coffeebeankorea.com/',
    'description': '',
    'telephone': '',
    'title': '<b>커피</b>빈 여의도<b>SK</b><b>증권</b>빌딩점'
}
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

    @retries(7, 5)
    def fetch_man_ready_matching(
        self,
        man_matching_id: str,
    ) -> Dict:
        man_matching_result = self.client.collection("matchings").document(man_matching_id).get()
        assert man_matching_result.to_dict().get("status") == "ready"

    @retries(7, 5)
    def fetch_woman_rearranged_matching(
        self,
        woman_matching_id: str,
    ) -> Dict:
        man_matching_result = self.client.collection("matchings").document(woman_matching_id).get()
        assert man_matching_result.to_dict().get("status") == "rearranged"
        
    @retries(4, 5)
    def fetch_man_matching_complete(
        self,
        man_matching_id: str,
    ) -> Dict:
        man_matching_result = self.client.collection("matchings").document(man_matching_id).get()
        print(man_matching_result.to_dict().get("status"))
        assert man_matching_result.to_dict().get("status") == "complete"
        
    @retries(3, 3)
    def activate_matching_data(
        self,
        woman_matching_id: str,
        man_matching_id: str,
    ) -> Dict:

        self.client.collection('matchings').document(woman_matching_id).update(
            {
                "is_active": True, 
                "women_status_ready_at": firestore.SERVER_TIMESTAMP,
                "confirm_time_limit": set_hour_24(),

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
        man_matching_id: str,
        preferred_region: str = '한남동',
        preferred_place_type: str = '레스토랑',
        manner_comment: str = "반갑습닏. 저는 커피도 식사도 좋아요 :-)",
    ) -> Dict:
        timelist = fetch_appointments_list()
        self.client.collection('matchings').document(woman_matching_id).update(
            {
                "status": "ready",
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
        self.client.collection('matchings').document(man_matching_id).update(
            {
                "status": "ready",
            }
        )
        
    def confirm_male_selected_place(
        self,
        man_matching_id: str,
        selected_place: str = DEFAULT_SELECTED_PLACE,
    ) -> Dict:
        selected_place = {
            'roadAddress': '서울특별시 영등포구 국제금융로8길 31 K-Tower 1층 105호, 106호',
            'link': 'http://www.coffeebeankorea.com/',
            'description': '',
            'telephone': '',
            'title': '<b>커피</b>빈 여의도<b>SK</b><b>증권</b>빌딩점'
        }
        self.client.collection('matchings').document(man_matching_id).update(
            {
                "male_confirmed_at": firestore.SERVER_TIMESTAMP,
                "selected_place": selected_place,
                "selected_appointment": set_hour_24(1)
            }
        )
    
    def back_status_ready_data(
        self,
        woman_matching_id: str,
    ) -> Dict:
        self.client.collection('matchings').document(woman_matching_id).update(
            {
                "women_status_ready_at": set_hour_24(-1),
                "confirm_time_limit": set_hour_24(-1),
            }
        )
    
    def rearrange_matching_place(
        self,
        man_matching_id: str,
        woman_matching_id: str, 
        preferred_region: str = '한남동',
        preferred_place_type: str = '레스토랑',
    ) -> Dict:
        timelist = fetch_appointments_list()
        self.client.collection('matchings').document(man_matching_id).update(
            {
                "status": "rearranged",
                "appointments": timelist,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "selected_place": {
                    "description": "",
                    "roadAddress": "서울특별시 강남구 논현로 854 안다즈호텔 지하 1층 112호",
                    "link": "https://app.catchtable.co.kr/ct/main/searchRedirect?key=0921_cheeseroom",
                    "title": "<b>치즈룸</b> 안다즈",
                    "telephone": "",
                }
            }
        )
        print(woman_matching_id, 'woman matching id')
        self.fetch_woman_rearranged_matching(woman_matching_id)

    def confirm_rearranged_time(
        self,
        woman_matching_id: str,
        man_matching_id,
        preferred_region: str = '한남동',
        preferred_place_type: str = '레스토랑',
    ) -> Dict:
        timelist = fetch_appointments_list()
        self.client.collection('matchings').document(woman_matching_id).update(
            {
                "selected_appointment": timelist[0],
                "status": "complete",
                "updated_at": firestore.SERVER_TIMESTAMP,
                "female_rearranged_confirmed_at": firestore.SERVER_TIMESTAMP,
                
            }
        )
        self.fetch_man_matching_complete(man_matching_id)

    def fetch_matching(
        self,
        matching_id: str,
    ) -> Dict:
        return self.client.collection('matchings').document(matching_id).get().to_dict()

    def fetch_matching_complete(
        self,
        man_uid: str,
        woamn_uid: str,
    ) -> Optional[Dict]:
        matching_compelte_list = (
            self.client.collection('matching_complete').where('male_user_uid', '==', man_uid).where("female_user_uid", '==', woamn_uid).get()
        )
        for x in matching_compelte_list:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            return datadict

