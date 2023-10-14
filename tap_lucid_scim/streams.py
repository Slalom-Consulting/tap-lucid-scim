"""Stream type classes for tap-lucid-scim."""

from __future__ import annotations

import typing as t
from pathlib import Path


from tap_lucid_scim.client import LucidScimStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UsersStream(LucidScimStream):
    """Define custom stream."""

    name = "users"
    path = "/Users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001


#class GroupsStream(LucidScimStream):
#    """Define custom stream."""
#
#    name = "groups"
#    path = "/Groups"
#    primary_keys: t.ClassVar[list[str]] = ["id"]
#    replication_key = None
#    schema_filepath = SCHEMAS_DIR / "groups.json"  # noqa: ERA001
