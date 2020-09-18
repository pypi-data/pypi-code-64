#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lockable Resources management application
"""
import logging
import functools

import requests.exceptions
from jenkinsapi.jenkins import Jenkins

from .model import LockableResources

INFO_STATE_COLORS = {
    'FREE': 'green',
    'RESERVED': 'yellow',
    'LOCKED': 'red'
}


def api_method(func):
    log = logging.getLogger(func.__name__)
    @functools.wraps(func)
    def wrapped(api, *args, **kwargs):
        try:
            return func(api, *args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            api.output.error('Failed to connect to {}. Check your connection and try again.'.format(e.request.url))
            log.error(e)
        except Exception as e:  # pylint: disable=broad-except
            api.output.error('{}'.format(e))
            log.exception(e)
    return wrapped


class Application():
    """
    Base Application context class for accessing.
    """
    def __init__(self, output, obj, interactive=False):
        """
        Instanciate the application

        Args:
            output: The outputer object
            obj: A backend object
            interactive: Set interactive to let prompt for user input
        """
        self.output = output
        self.interactive = interactive
        self.obj = obj

class LockableResourceApp(Application):
    """
    Application context class for accessing lockable resources in jenkins.
    """

    @classmethod
    def from_default(cls, output, jenkins_url, jenkins_user, jenkins_token,
                     filter_expr=None, interactive=False):
        """
        Default app creator using dependency injections
        - Instanciate Jenkins object
        - Instanciate LockableResources
        - Instanciate LockableResourceApp

        Args:
            output: The outputer object.
            jenkins_url: The url to jenkins instance
            jenkins_user: The user to authenticate to jenkins
            jenkins_token: The user token to use for authentication
            filter_expr: A filter expression to include only maching patterns of resources
            interactive: Set interactive to let prompt for user input

        Return:
            LockableResourceApp object
        """
        # Instanciate jenkins object
        jenkins = Jenkins(jenkins_url, jenkins_user, jenkins_token, lazy=True)
        mgr = LockableResources(jenkins, res_filter=filter_expr)

        return LockableResourceApp(output, mgr, interactive)

    @api_method
    def reserve(self, filter_expr=None, force=None):
        """
        Reserve a resource

        Args:
            filter_expr: Resource pattern to reserve. If not provided, reserve the first free.
        """
        # Issue a warning if you already have one resource owned
        owned = self.obj.get_owned_resources()
        if owned:
            self.output.warn('You already have one resource owned.')
            if force is None:
                if not self.output.confirm('Force reserving?'):
                    return
            elif not force:
                return

        # Find free resources in list
        reslist = self._get_matching_free_resources(filter_expr)
        if reslist and not filter_expr:
            reslist = reslist[:1]

        if not reslist:
            self.output.warn('Sorry, no free resources at the moment. Try again later.')
            return

        for res in reslist:
            res.reserve()
            self.output.info(f'Reserved {res.name}')

    @api_method
    def unreserve(self, filter_expr=None):
        """
        Unreserve a resource

        Args:
            filter_expr: Resource pattern to unreserve. If not provided, unreserve the resources owned by current user.
        """
        # Name provided: Find matching resources
        reslist = list(self.obj.values(filter_expr))
        if not reslist:
            raise Exception(f'No resources matching "{filter_expr}"')

        # Find owned resources in list
        reslist = [r for r in reslist if r.is_owned()]

        if not reslist:
            self.output.warn('No resources to release')
            return

        for res in reslist:
            res.unreserve()
            self.output.info(f'Unreserved {res.name}')

    @api_method
    def list(self, filter_expr=None, short_name=False):
        """
        List resources

        Args:
            filter_expr: Resource pattern to include
            short_name: Output to the short name version instead of full hostname
        """
        for res in self.obj.values(filter_expr):
            name = res.name
            if short_name:
                name = name.split('.')[0]
            self.output.info(name)

    @api_method
    def info(self, filter_expr=None):
        """
        Show info of resources

        Args:
            filter_expr: Resource pattern to include
        """
        for res in self.obj.values(filter_expr):
            state = res.state
            if not res.is_free():
                state += f' by {res.owner}'
            self.output.info(f'{res.name}: ', nl=False)
            self.output.info(f'{state}', fg=INFO_STATE_COLORS[res.state])

    @api_method
    def owned(self, user=None, short_name=False, count=None, index=None, reserve=False, reserve_filter=None):
        """
        List owned resources

        Args:
            user: Owner of resource
            short_name: Output to the short name version instead of full hostname
            count: the max number of owned resources to return
            index: the owned resource list position to select
            reserve: try to reserve a resource matching the string or any if no resource currently owned
            reserve_filter: Resource pattern to include
        """
        owned = self.obj.get_owned_resources(user)
        if not owned and reserve:

            free = self._get_matching_free_resources(reserve_filter)
            owned = free[:1]

            for res in owned:
                res.reserve()

        count = count or len(owned)
        if index is None:
            index = 0
        else:
            count = 1
        end = index + count

        for res in owned[index:end]:
            name = res.name
            if short_name:
                name = name.split('.')[0]
            self.output.info(name)

    def _get_matching_free_resources(self, filter_expr=r'.*'):
        # Find matchingn resources
        reslist = list(self.obj.values(filter_expr))
        if not reslist:
            raise Exception(f'No resources matching "{filter_expr}"')
        # Find free resources in list
        return [
            r for r in reslist if r.is_free()
        ]
