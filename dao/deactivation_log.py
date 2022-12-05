from typing import List
from .base_dao import BaseDao
from firebase_admin import firestore


class DeactivationDao(BaseDao):

    def insert_deactivation_log(
        self,
        uid,
        uid_list: List[str]
    ):
        current_timestamp = firestore.SERVER_TIMESTAMP
        self.client.collection("deactivation_log").add({
            'uid': uid,
            'deactivated_list': uid_list,
            'deactivated_at': current_timestamp,
            'created_at': current_timestamp
        })
