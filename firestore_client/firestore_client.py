import os
from typing import Any
from google.cloud.firestore import Client
from google.auth.credentials import AnonymousCredentials
from google.cloud.client import ClientWithProject  # type: ignore
import google.api_core.client_options
from google.api_core.gapic_v1 import client_info
from google.cloud.firestore_v1 import __version__


_FIRESTORE_EMULATOR_HOST: str = "FIRESTORE_EMULATOR_HOST"
_DEFAULT_EMULATOR_PROJECT = "google-cloud-firestore-emulator"
DEFAULT_DATABASE = "(default)"
_CLIENT_INFO: Any = client_info.ClientInfo(client_library_version=__version__)


class FirestoreClient(Client):

    def __init__(
        self,
        project=None,
        credentials=None,
        database=DEFAULT_DATABASE,
        client_info=_CLIENT_INFO,
        client_options=None,
        emulator_host=None
    ) -> None:
        # NOTE: This API has no use for the _http argument, but sending it
        #       will have no impact since the _http() @property only lazily
        #       creates a working HTTP object.
        super(Client, self).__init__(
            project=project,
            credentials=credentials,
            database=database,
            client_info=client_info,
            client_options=client_options,
        )
        self._emulator_host = emulator_host

        if self._emulator_host is not None:
            if credentials is None:
                credentials = AnonymousCredentials()
            if project is None:
                project = _DEFAULT_EMULATOR_PROJECT
        self._client_info = client_info
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
        self._client_options = client_options

        self._database = database