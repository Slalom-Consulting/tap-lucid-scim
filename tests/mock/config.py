"""Mock Config."""

from pathlib import Path

API_URL = "https://users.lucid.app/scim/v2"
MOCK_RESPONSE_DIR = Path(__file__).parent / Path("responses")

mocks = [
    {
        "type": "stream",  # "stream": "users",
        "url": API_URL + "/Users",
        "file": MOCK_RESPONSE_DIR.joinpath("users.json"),
    },
]
