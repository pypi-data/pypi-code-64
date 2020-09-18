#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
Lockable Resources CLI entrypoint
"""

import fnmatch
from functools import update_wrapper

import click

from . import VERSION
from .app import LockableResourceApp
from .config import ConfigLoader

DEFAULT_JENKINS_URL = 'https://127.0.0.1'


class ClickStreamer():

    """
    Provides interfaces for output formating and input prompting functionality using click utilities.
    """

    # pylint: disable=no-self-use
    def __call__(self, msg, **kwargs):
        click.secho(msg, **kwargs)

    def prompt(self, *args, **kwargs):
        return click.prompt(*args, **kwargs)

    def confirm(self, *args, **kwargs):
        return click.confirm(*args, **kwargs)

    def info(self, msg, fg='cyan', **kwargs):
        click.secho(msg, fg=fg, **kwargs)

    def highlight(self, msg, fg='purple', **kwargs):
        click.secho(msg, fg=fg, **kwargs)

    def warn(self, msg, fg='yellow', **kwargs):
        click.secho(f'WARN: {msg}', fg=fg, **kwargs)

    def error(self, msg, fg='red', **kwargs):
        click.secho(f'ERROR: {msg}', fg=fg, **kwargs)


default_streamer = ClickStreamer()


class AppFactory():
    """
    Application Factory wrapper.

    This class provides a simple factory pattern to create the application only if needed.
    """

    def __init__(self, ctor, *args, **kwargs):
        """
        Instantiates a instance of AppFactory

        Args:
            ctor (callable): The constructor function to instanciate the application. This can be a function or a class.
            args: The positionnal arguments to provide to the constructor when instantiating.
            kwargs: The named arguments to provide to the constructor when instantiating.

        The factory provides the property `app` that holds the application instance. The application will be created
        when accessing the property the first time.
        """
        self._app = None
        self._ctor = ctor
        self._args = args
        self._kwargs = kwargs

    @property
    def app(self):
        if not self._app:
            self._app = self.create_app()
        return self._app

    def create_app(self):
        return self._ctor(*self._args, **self._kwargs)


def pass_app(f):
    """
    Decorator to only pass the application from factory.
    """
    def new_func(*args, **kwargs):
        ctx = click.get_current_context()
        obj = ctx.ensure_object(AppFactory)
        return f(obj.app, *args, **kwargs)

    return update_wrapper(new_func, f)

def click_completion_install_option(f):

    if 'click_completion' in sys.modules:

        def completion_install(ctx, attr, value):  # pylint: disable=inconsistent-return-statements
            if not value or ctx.resilient_parsing:
                return value
            shell, path = click_completion.core.install()
            click.echo('%s completion installed in %s' % (shell, path))
            sys.exit(0)
        # Add autocompletion auto install support if click autocomplete is installed
        click_completion.init()

        f = click.option('--install-completion',
                         is_flag=True,
                         callback=completion_install,
                         expose_value=False,
                         help='Install shell auto completion')(f)
    return f

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()

CONFIG_PATHS = (
    '/etc/lockable-resources.yml',
    '~/.lockable-resources.yml',
    '.lockable-resources.yml'
)
CONTEXT_SETTINGS = ConfigLoader(CONFIG_PATHS).click_settings

@click.group('resource', context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('--jenkins-url', help='Jenkins URL', default=DEFAULT_JENKINS_URL, envvar=['JENKINS_URL', 'JENKINS_HOST'],
              show_envvar=True)
@click.option('--jenkins-user', '-u', help='Jenkins User used to connect to jenkins',
              envvar='JENKINS_USER', show_envvar=True, prompt=True)
@click.option('--jenkins-token', '-T', help='Jenkins token used to authenticate to jenkins',
              envvar='JENKINS_TOKEN', prompt=True, hide_input=True)
@click.option('--filter', '-f', 'filter_expr', help='Global resources filter',
              show_default=True)
@click.option('--interactive', '-i', is_flag=True, default=False, help='Enables interactive input prompts')
@click.pass_context
def cli(ctx, jenkins_url, jenkins_user, jenkins_token, filter_expr, interactive):
    ctx.obj = AppFactory(LockableResourceApp.from_default, default_streamer, jenkins_url, jenkins_user, jenkins_token,
                         filter_expr, interactive)


@cli.command()
@click.argument('pattern', required=False)
@click.option('--regex', '-e', 'regex', help='Regex filter pattern for resources')
@pass_app
def reserve(app, pattern, regex):
    '''Reserve a resource for current user.  If PATTERN is not provided, reserve the first free resource.'''
    if pattern and not regex:
        regex = fnmatch.translate(pattern)
    app.reserve(regex)


@cli.command()
@click.argument('pattern', required=False)
@click.option('--regex', '-e', 'regex', help='Regex filter pattern for resources')
@pass_app
def unreserve(app, pattern, regex):
    '''Unreserve a resource from current user. If PATTERN is not provided, releases all owned resources.'''
    if pattern and not regex:
        regex = fnmatch.translate(pattern)
    app.unreserve(regex)


@cli.command('list')
@click.argument('pattern', required=False)
@click.option('--short-name', '-s', is_flag=True, help='Output to a short name if possible')
@click.option('--regex', '-e', 'regex', help='Regex filter pattern for resources')
@pass_app
def list_(app, pattern, short_name, regex):
    '''List all available resources matching PATTERN if set.'''
    if pattern and not regex:
        regex = fnmatch.translate(pattern)
    app.list(regex, short_name)


@cli.command()
@click.argument('pattern', required=False)
@click.option('--regex', '-e', 'regex', help='Regex filter pattern for resources')
@pass_app
def info(app, pattern, regex):
    '''
    Show info of all available resources matching PATTERN if set.
    '''
    if pattern and not regex:
        regex = fnmatch.translate(pattern)
    app.info(regex)


@cli.command()
@click.option('--user', '-u', help='User owning the boards (default to jenkins-user)')
@click.option('--short-name', '-s', is_flag=True, help='Output to a short name if possible')
@click.option('--count', '-c', type=int, default=None, help='Max number of owned resources to display')
@click.option('--index', '-i', type=int, default=None, help='Position of owned resource in list to select')
@click.option('--reserve', '-r', 'auto_reserve', is_flag=True, help='Auto reserve a resource if none owned')
@click.option('--reserve-pattern', '-p', help='Fnmatch pattern to match resources to reserve')
@click.option('--reserve-regex', '-e', help='Regex pattern to match resources to reserve')
@pass_app
def owned(app, user, short_name, count, index, auto_reserve, reserve_pattern, reserve_regex):
    '''List owned resources by <user>.'''
    if reserve_pattern and not reserve_regex:
        reserve_regex = fnmatch.translate(reserve_pattern)
    app.owned(user, short_name, count, index, auto_reserve, reserve_regex)


@cli.command()
@pass_app
def launch(app):
    '''Lunches the web site of resources.'''
    click.launch(app.resources.baseurl, wait=False)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
