"""Pagination handling for LucidScimStream."""

from requests import Response
from singer_sdk.pagination import BaseOffsetPaginator


class LucidScimPaginator(BaseOffsetPaginator):
    def has_more(self, response: Response) -> bool:
        page_info = response.json() or {}
        self._page_size = page_info["itemsPerPage"]
        total_results = page_info["totalResults"]
        return self.get_next(response) < total_results
