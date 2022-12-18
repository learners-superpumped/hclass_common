from typing import Dict
from .base_dao import BaseDao


class UserTestDao(BaseDao):

    def fetch_all_user_test_map(self) -> Dict[str, bool]:
        user_col_ref = self.client.collection("users_test")
        result = user_col_ref.stream()
        user_map = {}
        for data in result:
            data_dict = data.to_dict()
            user_map[data_dict.get('uid', '')] = True
        return user_map