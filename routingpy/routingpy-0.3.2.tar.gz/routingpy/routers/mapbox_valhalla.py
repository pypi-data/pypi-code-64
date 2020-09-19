# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from .valhalla import Valhalla
from .base import DEFAULT


class MapboxValhalla(Valhalla):
    """Performs requests to Mapbox's Valhalla instance."""

    _base_url = 'https://api.mapbox.com/valhalla/v1'

    def __init__(
        self,
        api_key,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        requests_kwargs=None,
        retry_over_query_limit=False,
        skip_api_error=None
    ):
        """
        Initializes a Valhalla client.

        :param api_key: Mapbox API key.
        :type api_key: str

        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.
        :type user_agent: str

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify ``None`` for no timeout. Default :attr:`routingpy.routers.options.default_timeout`.
        :type timeout: int or None

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.  Default :attr:`routingpy.routers.options.default_retry_timeout`.
        :type retry_timeout: int

        :param requests_kwargs: Extra keyword arguments for the requests
            library, which among other things allow for proxy auth to be
            implemented. **Note**, that ``proxies`` can be set globally
            in :attr:`routingpy.routers.options.default_proxies`.

            Example:

            >>> from routingpy.routers import MapboxValhalla
            >>> router = MapboxValhalla(my_key, requests_kwargs={
            >>>     'proxies': {'https': '129.125.12.0'}
            >>> })
            >>> print(router.proxies)
            {'https': '129.125.12.0'}
        :type requests_kwargs: dict

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_over_query_limit`.
        :type retry_over_query_limit: bool

        :param skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.
        :type skip_api_error: bool
        """

        super(MapboxValhalla, self).__init__(
            self._base_url, api_key, user_agent, timeout, retry_timeout, requests_kwargs,
            retry_over_query_limit, skip_api_error
        )
