from hclass_common.firestore_client.firestore_client import FirestoreClient


class BaseDao(object):

    def __init__(self, client: FirestoreClient):
        self.client: FirestoreClient = client