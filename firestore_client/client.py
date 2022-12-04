from google.cloud.firestore import Client
from .firestore_client import FirestoreClient
from firebase_admin import credentials
from contextlib import contextmanager


test_client: Client = FirestoreClient(
    project='h-class',
    emulator_host='host.docker.internal:8080'
)
cred = credentials.Certificate('hclass.json')
production_client: Client = FirestoreClient(
    project='h-class',
)


def get_firebase_client() -> FirestoreClient:
    try:
        cred = credentials.Certificate('hclass.json')
        client =  FirestoreClient(
            project='h-class',
        )
        yield client
    finally:
        client.close()


@contextmanager
def get_firebase_client_context():
    try:
        cred = credentials.Certificate('hclass.json')
        client =  FirestoreClient(
            project='h-class',
        )
        yield client
    finally:
        client.close()

def get_firebase_test_client() -> FirestoreClient:
    try:
        client =  FirestoreClient(
            project='h-class',
            emulator_host='host.docker.internal:8080'
        )
        yield client
    finally:
        client.close()
