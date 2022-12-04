from typing import Dict
from .base_dao import BaseDao


class EvaluationDao(BaseDao):

    def fetch_evaluation(self, uid: str) -> Dict:
        result = self.client.collection("evaluations").where('uid', '==', uid).get()
        result = result[0]
        return result.to_dict()
