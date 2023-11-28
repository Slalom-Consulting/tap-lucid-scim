"""Stream type classes for tap-lucid-scim."""

from __future__ import annotations

import typing as t
from pathlib import Path

from tap_lucid_scim.client import LucidScimStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UsersStream(LucidScimStream):
    """Users stream."""

    name = "users"
    path = "/Users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR.joinpath("users.json")


class GroupsStream(LucidScimStream):
    """Groups stream."""

    name = "groups"
    path = "/Groups"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR.joinpath("groups.json")
