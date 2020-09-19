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
#

from typing import List

from .base import Router, DEFAULT
from routingpy import convert, utils
from routingpy.direction import Directions, Direction
from routingpy.matrix import Matrix


class OSRM(Router):
    """Performs requests to the OSRM API services."""

    _DEFAULT_BASE_URL = 'https://router.project-osrm.org'

    def __init__(
        self,
        base_url=_DEFAULT_BASE_URL,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        requests_kwargs=None,
        retry_over_query_limit=False,
        skip_api_error=None
    ):
        """
        Initializes an OSRM client.

        :param base_url: The base URL for the request. Defaults to the OSRM demo API
            server. Should not have a trailing slash.
        :type base_url: str

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

            >>> from routingpy.routers import OSRM
            >>> router = OSRM(my_key, requests_kwargs={
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

        super(OSRM, self).__init__(
            base_url, user_agent, timeout, retry_timeout, requests_kwargs, retry_over_query_limit,
            skip_api_error
        )

    def directions(
        self,
        locations,
        profile,
        radiuses=None,
        bearings=None,
        alternatives=None,
        steps=None,
        continue_straight=None,
        annotations=None,
        geometries=None,
        overview=None,
        dry_run=None
    ):
        """Get directions between an origin point and a destination point.

        For more information, visit http://project-osrm.org/docs/v5.5.1/api/#route-service.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["car", "bike", "foot"].
        :type profile: str

        :param radiuses: A list of maximum distances (measured in
            meters) that limit the search of nearby road segments to every given waypoint.
            The values must be greater than 0, an empty element signifies to use the backend default
            radius. The number of radiuses must correspond to the number of waypoints.
        :type radiuses: list of int

        :param bearings: Specifies a list of pairs (bearings and
            deviations) to filter the segments of the road network a waypoint can
            snap to. For example bearings=[[45,10],[120,20]]. Each pair is a
            comma-separated list that can consist of one or two float values, where
            the first value is the bearing and the second one is the allowed deviation
            from the bearing. The bearing can take values between 0 and 360 clockwise
            from true north. If the deviation is not set, then the default value of
            100 degrees is used. The number of pairs must correspond to the number
            of waypoints.
        :type bearings: list of list

        :param alternatives: Search for alternative routes. A result cannot be guaranteed. Accepts an integer or False.
            Default False.
        :type alternatives: bool or int

        :param steps: Return route steps for each route leg. Default false.
        :type steps: bool

        :param continue_straight: Forces the route to keep going straight at waypoints constraining
            uturns there even if it would be faster. Default value depends on the profile.
        :type continue_straight: bool

        :param annotations: Returns additional metadata for each coordinate along the route geometry. Default false.
        :type annotations: bool

        :param geometries: Returned route geometry format (influences overview and per step). One of ["polyline",
            "polyline6", "geojson". Default polyline.
        :type geometries: str

        :param overview: Add overview geometry either full, simplified according to highest zoom level
            it could be display on, or not at all. One of ["simplified", "full", "false", False]. Default simplified.
        :type overview: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """

        coords = convert._delimit_list(
            [convert._delimit_list([convert._format_float(f) for f in pair]) for pair in locations], ';'
        )

        params = dict()

        if radiuses:
            params["radiuses"] = convert._delimit_list(radiuses, ';')

        if bearings:
            params["bearings"] = convert._delimit_list(
                [convert._delimit_list(pair) for pair in bearings], ';'
            )

        if alternatives is not None:
            params["alternatives"] = convert._convert_bool(alternatives)

        if steps is not None:
            params["steps"] = convert._convert_bool(steps)

        if continue_straight is not None:
            params["continue_straight"] = convert._convert_bool(continue_straight)

        if annotations is not None:
            params["annotations"] = convert._convert_bool(annotations)

        if geometries:
            params["geometries"] = geometries

        if overview is not None:
            params["overview"] = convert._convert_bool(overview)

        return self._parse_direction_json(
            self._request("/route/v1/" + profile + '/' + coords, get_params=params, dry_run=dry_run),
            alternatives, geometries
        )

    @staticmethod
    def _parse_direction_json(response, alternatives, geometry_format):
        if response is None:  # pragma: no cover
            if alternatives:
                return Directions()
            else:
                return Direction()

        def _parse_geometry(route_geometry):
            if geometry_format in (None, 'polyline'):
                geometry = utils.decode_polyline5(route_geometry, is3d=False)
            elif geometry_format == 'polyline6':
                geometry = utils.decode_polyline6(route_geometry, is3d=False)
            elif geometry_format == 'geojson':
                geometry = route_geometry['coordinates']
            else:
                raise ValueError(
                    "OSRM: parameter geometries needs one of ['polyline', 'polyline6', 'geojson"
                )
            return geometry

        if alternatives:
            routes = []
            for route in response['routes']:
                routes.append(
                    Direction(
                        geometry=_parse_geometry(route['geometry']),
                        duration=int(route['duration']),
                        distance=int(route['distance']),
                        raw=route
                    )
                )
            return Directions(routes, response)
        else:
            return Direction(
                geometry=_parse_geometry(response['routes'][0]['geometry']),
                duration=int(response['routes'][0]['duration']),
                distance=int(response['routes'][0]['distance']),
                raw=response
            )

    def isochrones(self):  # pragma: no cover
        raise NotImplementedError

    def matrix(
        self,
        locations,
        profile,
        radiuses=None,
        bearings=None,
        sources=None,
        destinations=None,
        dry_run=None,
        annotations=['duration', 'distance']
    ):
        """
        Gets travel distance and time for a matrix of origins and destinations.

        For more information visit http://project-osrm.org/docs/v5.5.1/api/#table-service.

        :param locations: The coordinates tuple the route should be calculated
            from.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["car", "bike", "foot"].
        :type profile: str

        :param radiuses: A list of maximum distances (measured in
            meters) that limit the search of nearby road segments to every given waypoint.
            The values must be greater than 0, an empty element signifies to use the backend default
            radius. The number of radiuses must correspond to the number of waypoints.
        :type radiuses: list of int

        :param bearings: Specifies a list of pairs (bearings and
            deviations) to filter the segments of the road network a waypoint can
            snap to. For example bearings=[[45,10],[120,20]]. Each pair is a
            comma-separated list that can consist of one or two float values, where
            the first value is the bearing and the second one is the allowed deviation
            from the bearing. The bearing can take values between 0 and 360 clockwise
            from true north. If the deviation is not set, then the default value of
            100 degrees is used. The number of pairs must correspond to the number
            of waypoints.
        :type bearings: list of list

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list of int

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list of int

        :param dry_run: Print URL and parameters without sending the request.
        :type dry_run: bool

        :param annotations: Return the requested table or tables in response.
            One or more of ["duration", "distance"].
        :type annotations: List[str]

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`

        .. versionchanged:: 0.3.0
           Add annotations parameter to get both distance and duration
        """

        coords = convert._delimit_list(
            [convert._delimit_list([convert._format_float(f) for f in pair]) for pair in locations], ';'
        )

        params = dict()

        if sources:
            params['sources'] = convert._delimit_list(sources, ';')

        if destinations:
            params['destinations'] = convert._delimit_list(destinations, ';')

        if annotations:
            params['annotations'] = convert._delimit_list(annotations)

        return self._parse_matrix_json(
            self._request("/table/v1/" + profile + '/' + coords, get_params=params, dry_run=dry_run)
        )

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:  # pragma: no cover
            return Matrix()

        return Matrix(
            durations=response.get('durations'), distances=response.get('distances'), raw=response
        )
