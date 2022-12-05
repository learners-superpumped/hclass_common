from typing import Dict, Optional
from .base_dao import BaseDao


class LastCalculationDao(BaseDao):

    def fetch_last_action_log(self, uid: str) -> Optional[Dict]:
        calclog = self.client.collection('last_action_log').where('uid', '==', uid).get()
        new_data_list = []
        for x in calclog:
            datadict = x.to_dict()
            datadict['dataid'] = x.id
            new_data_list.append(datadict)
        new_data_list = sorted(new_data_list, key=lambda x: x.get('last_action_time'), reverse=True)
        if new_data_list:
            return new_data_list[0]
        return None

    def insert_last_action(self, datadict: Dict) -> Optional[Dict]:
        self.client.collection('last_action_log').add(datadict)
        
    def update_last_action(self, dataid: str, datadict: Dict) -> Optional[Dict]:
        self.client.collection('last_action_log').document(dataid).update(datadict)
