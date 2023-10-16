"""LucidScim tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_lucid_scim import streams


class TapLucidScim(Tap):
    """LucidScim tap class."""

    name = "tap-lucid-scim"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "stream_config",
            th.ObjectType(
                additional_properties=th.ObjectType(
                    th.Property(
                        "parameters",
                        th.StringType,
                        description="URL formatted parameters string to \
                            be used for stream.",
                    ),
                )
            ),
            description="Custom configuration for streams.",
        ),
        th.Property(
            'page_size',
            th.IntegerType,
            default=None,
            description='Result limit for paginated streams'
        ),
        th.Property(
            "api_url",
            th.StringType,
            default=None,
            description="Override the url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.LucidScimStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
        #    streams.GroupsStream(self),
            streams.UsersStream(self),
        ]


if __name__ == "__main__":
    TapLucidScim.cli()
