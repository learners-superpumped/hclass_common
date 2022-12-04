from typing import Dict
from .base_dao import BaseDao
from firebase_admin import auth


class UserDao(BaseDao):

    def fetch_user(self, uid: str) -> Dict:
        result = self.client.collection("users").where('uid', '==', uid).get()
        result = result[0]
        return result.to_dict()
