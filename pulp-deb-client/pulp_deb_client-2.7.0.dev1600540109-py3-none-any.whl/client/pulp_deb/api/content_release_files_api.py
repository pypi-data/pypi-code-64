# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pulpcore.client.pulp_deb.api_client import ApiClient
from pulpcore.client.pulp_deb.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class ContentReleaseFilesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create(self, deb_release_file, **kwargs):  # noqa: E501
        """Create a release file  # noqa: E501

        A ReleaseFile represents the Release file(s) from a single APT distribution.  Associated artifacts: At least one of 'Release' and 'InRelease' file. If the 'Release' file is present, then there may also be a 'Release.gpg' detached signature file for it.  Note: The verbatim publisher will republish all associated artifacts, while the APT publisher (both simple and structured mode) will generate any 'Release' files it needs when creating the publication. It does not make use of ReleaseFile content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create(deb_release_file, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param DebReleaseFile deb_release_file: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DebReleaseFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_with_http_info(deb_release_file, **kwargs)  # noqa: E501

    def create_with_http_info(self, deb_release_file, **kwargs):  # noqa: E501
        """Create a release file  # noqa: E501

        A ReleaseFile represents the Release file(s) from a single APT distribution.  Associated artifacts: At least one of 'Release' and 'InRelease' file. If the 'Release' file is present, then there may also be a 'Release.gpg' detached signature file for it.  Note: The verbatim publisher will republish all associated artifacts, while the APT publisher (both simple and structured mode) will generate any 'Release' files it needs when creating the publication. It does not make use of ReleaseFile content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_with_http_info(deb_release_file, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param DebReleaseFile deb_release_file: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DebReleaseFileResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'deb_release_file'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'deb_release_file' is set
        if self.api_client.client_side_validation and ('deb_release_file' not in local_var_params or  # noqa: E501
                                                        local_var_params['deb_release_file'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `deb_release_file` when calling `create`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'deb_release_file' in local_var_params:
            body_params = local_var_params['deb_release_file']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/content/deb/release_files/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DebReleaseFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list(self, **kwargs):  # noqa: E501
        """List release files  # noqa: E501

        A ReleaseFile represents the Release file(s) from a single APT distribution.  Associated artifacts: At least one of 'Release' and 'InRelease' file. If the 'Release' file is present, then there may also be a 'Release.gpg' detached signature file for it.  Note: The verbatim publisher will republish all associated artifacts, while the APT publisher (both simple and structured mode) will generate any 'Release' files it needs when creating the publication. It does not make use of ReleaseFile content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str codename: codename
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str ordering: Which field to use when ordering the results.
        :param str relative_path: relative_path
        :param str repository_version: repository_version
        :param str repository_version_added: repository_version_added
        :param str repository_version_removed: repository_version_removed
        :param str sha256: sha256
        :param str suite: suite
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_with_http_info(**kwargs)  # noqa: E501

    def list_with_http_info(self, **kwargs):  # noqa: E501
        """List release files  # noqa: E501

        A ReleaseFile represents the Release file(s) from a single APT distribution.  Associated artifacts: At least one of 'Release' and 'InRelease' file. If the 'Release' file is present, then there may also be a 'Release.gpg' detached signature file for it.  Note: The verbatim publisher will republish all associated artifacts, while the APT publisher (both simple and structured mode) will generate any 'Release' files it needs when creating the publication. It does not make use of ReleaseFile content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str codename: codename
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str ordering: Which field to use when ordering the results.
        :param str relative_path: relative_path
        :param str repository_version: repository_version
        :param str repository_version_added: repository_version_added
        :param str repository_version_removed: repository_version_removed
        :param str sha256: sha256
        :param str suite: suite
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(InlineResponse2007, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'codename',
            'limit',
            'offset',
            'ordering',
            'relative_path',
            'repository_version',
            'repository_version_added',
            'repository_version_removed',
            'sha256',
            'suite',
            'fields',
            'exclude_fields'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'codename' in local_var_params and local_var_params['codename'] is not None:  # noqa: E501
            query_params.append(('codename', local_var_params['codename']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'ordering' in local_var_params and local_var_params['ordering'] is not None:  # noqa: E501
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501
        if 'relative_path' in local_var_params and local_var_params['relative_path'] is not None:  # noqa: E501
            query_params.append(('relative_path', local_var_params['relative_path']))  # noqa: E501
        if 'repository_version' in local_var_params and local_var_params['repository_version'] is not None:  # noqa: E501
            query_params.append(('repository_version', local_var_params['repository_version']))  # noqa: E501
        if 'repository_version_added' in local_var_params and local_var_params['repository_version_added'] is not None:  # noqa: E501
            query_params.append(('repository_version_added', local_var_params['repository_version_added']))  # noqa: E501
        if 'repository_version_removed' in local_var_params and local_var_params['repository_version_removed'] is not None:  # noqa: E501
            query_params.append(('repository_version_removed', local_var_params['repository_version_removed']))  # noqa: E501
        if 'sha256' in local_var_params and local_var_params['sha256'] is not None:  # noqa: E501
            query_params.append(('sha256', local_var_params['sha256']))  # noqa: E501
        if 'suite' in local_var_params and local_var_params['suite'] is not None:  # noqa: E501
            query_params.append(('suite', local_var_params['suite']))  # noqa: E501
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/content/deb/release_files/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2007',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read(self, deb_release_file_href, **kwargs):  # noqa: E501
        """Inspect a release file  # noqa: E501

        A ReleaseFile represents the Release file(s) from a single APT distribution.  Associated artifacts: At least one of 'Release' and 'InRelease' file. If the 'Release' file is present, then there may also be a 'Release.gpg' detached signature file for it.  Note: The verbatim publisher will republish all associated artifacts, while the APT publisher (both simple and structured mode) will generate any 'Release' files it needs when creating the publication. It does not make use of ReleaseFile content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(deb_release_file_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str deb_release_file_href: (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DebReleaseFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.read_with_http_info(deb_release_file_href, **kwargs)  # noqa: E501

    def read_with_http_info(self, deb_release_file_href, **kwargs):  # noqa: E501
        """Inspect a release file  # noqa: E501

        A ReleaseFile represents the Release file(s) from a single APT distribution.  Associated artifacts: At least one of 'Release' and 'InRelease' file. If the 'Release' file is present, then there may also be a 'Release.gpg' detached signature file for it.  Note: The verbatim publisher will republish all associated artifacts, while the APT publisher (both simple and structured mode) will generate any 'Release' files it needs when creating the publication. It does not make use of ReleaseFile content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(deb_release_file_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str deb_release_file_href: (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DebReleaseFileResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'deb_release_file_href',
            'fields',
            'exclude_fields'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'deb_release_file_href' is set
        if self.api_client.client_side_validation and ('deb_release_file_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['deb_release_file_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `deb_release_file_href` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'deb_release_file_href' in local_var_params:
            path_params['deb_release_file_href'] = local_var_params['deb_release_file_href']  # noqa: E501

        query_params = []
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '{deb_release_file_href}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DebReleaseFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
