from typing import Dict, List
import pandas as pd
from .base_dao import BaseDao


class UserDao(BaseDao):

    def fetch_user(self, uid: str) -> Dict:
        result = self.client.collection("users").where('uid', '==', uid).get()
        result = result[0]
        return result.to_dict()

    def fetch_active_woman_list(self) -> List[Dict]:
        user_col_ref = self.client.collection("users")
        result = user_col_ref.where('is_passed', '==', True).where('gender', '==', '여성').where('is_active', '==', True).stream()
        user_list = []
        for data in result:
            user_list.append(data.to_dict())
        return user_list

    def fetch_active_man_list(self) -> List[Dict]:
        user_col_ref = self.client.collection("users")
        result = user_col_ref.where('gender', '==', '남성').where('is_active', '==', True).stream()
        user_list = []
        for data in result:
            user_list.append(data.to_dict())
        return user_list

    def fetch_all_users_df(self) -> pd.DataFrame:
        user_col_ref = self.client.collection("users")
        result = user_col_ref.stream()
        user_list = []
        for data in result:
            user_list.append(data.to_dict())
        return pd.DataFrame(user_list)

    def fetch_all_user_map(self) -> Dict[str, Dict]:
        user_col_ref = self.client.collection("users")
        result = user_col_ref.stream()
        user_map = {}
        for data in result:
            user_map[data.id] = data.to_dict()
        return user_map