"""REST client handling, including LucidScimStream base class."""

from __future__ import annotations

from typing import Any, Callable
from urllib.parse import parse_qsl

import requests
from memoization import cached
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import RESTStream

from tap_lucid_scim.pagination import LucidScimPaginator

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


class LucidScimStream(RESTStream):
    """LucidScim stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        api_url = "https://users.lucid.app/scim/v2"
        url = self.config.get("api_url", api_url)
        return url

    records_jsonpath = "$.Resources[*]"

    @property
    @cached
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_new_paginator(self) -> LucidScimPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return LucidScimPaginator(start_value=1, page_size=0)

    # TODO: add backoff
    # https://lucidchart.zendesk.com/hc/en-us/community/posts/8678361152020-Rate-Limit-for-Lucid-chart-SCIM-API-s
    # 100 request/minute limit with 429 code

    def get_stream_config(self) -> dict:
        """Get config for stream."""
        stream_configs = self.config.get("stream_config", {})
        return stream_configs.get(self.name, {})

    def get_stream_params(self) -> dict:
        """Get parameters set in config for stream."""
        stream_params = self.get_stream_config().get("parameters", "") or ""
        return {qry[0]: qry[1] for qry in parse_qsl(stream_params.lstrip("?"))}

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = self.get_stream_params()

        if next_page_token:
            params["startIndex"] = next_page_token

        count = self.config.get("page_size")
        if count:
            params["count"] = count

        return params
