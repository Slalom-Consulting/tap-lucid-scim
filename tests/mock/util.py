"""Mock API."""

import json

import requests_mock

from tests.mock.config import mocks


def mock_api(func, tap_config):
    """Mock API."""

    def set_mock(mocker, mock_config: dict) -> None:
        with open(mock_config["file"], "r") as f:
            response = json.load(f)

        mock_type = mock_config["type"]
        url = mock_config["url"]

        if mock_type == "auth":
            mocker.post(url, json=response)

        elif mock_type == "stream":
            mocker.get(url, json=response)

    def wrapper():
        with requests_mock.Mocker() as m:
            for mock in mocks:
                set_mock(m, mock)

            func()

    wrapper()
