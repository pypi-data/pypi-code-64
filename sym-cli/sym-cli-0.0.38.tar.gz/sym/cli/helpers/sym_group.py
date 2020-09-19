import logging
from contextlib import ExitStack
from typing import Any, Callable, ClassVar, List

from click import Command, Context, Group
from sentry_sdk.api import push_scope

from ..errors import get_active_env_vars
from ..saml_clients.chooser import choose_saml_client
from . import segment
from .tee import Tee, TeeStdErr, TeeStdOut


class AutoTagCommand(Command):
    """
    A command where each invocation sets the Sentry tag with the
    command's name automatically. Additionally, any CliErrors
    raised from the command are logged.
    """

    def invoke(self, ctx: Context) -> Any:
        segment.track(
            "Command Executed", command=ctx.info_name, options=ctx.obj.to_dict()
        )
        with push_scope() as scope:
            scope.set_tag("command", ctx.info_name)
            scope.set_extra("options", ctx.obj.to_dict())
            return super().invoke(ctx)

    def parse_args(self, ctx, args):
        if (
            self.params
            and (resource := ctx.parent.params.get("resource"))
            and self.params[0].name == "resource"
            and (
                not args
                or not choose_saml_client(
                    ctx.parent.params["saml_client_name"]
                ).validate_resource(args[0])
            )
        ):
            args = [resource] + args
        return super().parse_args(ctx, args)

    def format_epilog(self, ctx, formatter):
        if not self.epilog:
            formatter.write(get_active_env_vars())
        super().format_epilog(ctx, formatter)


class SymGroup(Group):
    """
    A group where any defined commands automatically use
    AutoTagCommand.
    """

    tees: ClassVar[List[Tee]] = []

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)

    def __del__(self):
        self.__class__.reset_tees()

    @classmethod
    def reset_tees(cls):
        for tee in cls.tees:
            tee.close()
        cls.tees = []

    def invoke(self, ctx: Context) -> Any:
        if (log_dir := ctx.params.get("log_dir")) :
            # Don't register exit handler so exceptions are teed.
            # Instead, __del__ will be called when the program exits.
            self.__class__.tees.extend((TeeStdOut(log_dir), TeeStdErr(log_dir)))
            logging_filename = Tee.path_for_fd(log_dir, "logging")
        else:
            logging_filename = None

        if ctx.params.get("debug"):
            logging.basicConfig(level=logging.DEBUG, filename=logging_filename)
            logging.getLogger("segment").setLevel(logging.WARNING)

        return super().invoke(ctx)

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=AutoTagCommand)  # type: ignore
