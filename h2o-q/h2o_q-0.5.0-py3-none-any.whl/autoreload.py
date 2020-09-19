# This is a standalone, minimal version of the Tornado autoreload module ported from IOLoop to asyncio.
# There is no dependency on Tornado.
#
# Original implementation: https://github.com/tornadoweb/tornado/blob/master/tornado/autoreload.py

#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Automatically restart the server when a source file is modified.
"""

import os
import sys
import asyncio

# sys.path handling
# -----------------
#
# If a module is run with "python -m", the current directory (i.e. "")
# is automatically prepended to sys.path, but not if it is run as
# "path/to/file.py".  The processing for "-m" rewrites the former to
# the latter, so subsequent executions won't have the same path as the
# original.
#
# Conversely, when run as path/to/file.py, the directory containing
# file.py gets added to the path, which can cause confusion as imports
# may become relative in spite of the future import.
#
# We address the former problem by reconstructing the original command
# line (Python >= 3.4) or by setting the $PYTHONPATH environment
# variable (Python < 3.4) before re-execution so the new process will
# see the correct path.  We attempt to address the latter problem when
# h2o_q.autoreload is run as __main__.

if __name__ == "__main__":
    # This sys.path manipulation must come before our imports (as much
    # as possible - if we introduced a h2o_q.sys or h2o_q.os
    # module we'd be in trouble), or else our imports would become
    # relative again despite the future import.
    #
    # There is a separate __main__ block at the end of the file to call main().
    if sys.path[0] == os.path.dirname(__file__):
        del sys.path[0]

import math
import functools
import logging
import os
import pkgutil  # type: ignore
import sys
import traceback
import types
import subprocess
import weakref
from typing import Callable, Dict, List, Optional, Any, Mapping

logger = logging.getLogger('h2o_q.autoreload')

try:
    import signal
except ImportError:
    signal = None  # type: ignore

# os.execv is broken on Windows and can't properly parse command line
# arguments and executable name if they contain whitespaces. subprocess
# fixes that behavior.
_has_execv = sys.platform != "win32"

_watched_files = set()
_reload_hooks = []
_reload_attempted = False
_io_loops = weakref.WeakKeyDictionary()  # type: ignore
_autoreload_is_main = False
_original_argv = None  # type: Optional[List[str]]
_original_spec = None


def rerun(code: Any, glob: Dict[str, Any], loc: Optional[Optional[Mapping[str, Any]]] = None) -> None:
    if isinstance(code, str):
        # exec(string) inherits the caller's future imports; compile
        # the string first to prevent that.
        code = compile(code, "<string>", "exec", dont_inherit=True)
    exec(code, glob, loc)


class _Poll:
    """Schedules the given callback to be called periodically.

    The callback is called every ``interval_ms`` milliseconds.
    Note that the timeout is given in milliseconds, while most other
    time-related functions in Tornado use seconds.

    If the callback runs for longer than ``interval_ms`` milliseconds,
    subsequent invocations will be skipped to get back on schedule.

    `start` must be called after the `_Poll` is created.
    """

    def __init__(self, callback: Callable[[], None], interval_ms: float) -> None:
        self.callback = callback
        if interval_ms <= 0:
            raise ValueError("interval_ms must be positive")
        self.interval_ms = interval_ms
        self._running = False
        self._timeout: Optional[asyncio.TimerHandle] = None
        self.io_loop: Optional[asyncio.AbstractEventLoop] = None
        self._next_timeout = 0.0

    def start(self) -> None:
        """Starts the timer."""
        # Looking up the event loop here allows to first instantiate the
        # _Poll in another thread, then start it using call_at().
        self.io_loop = asyncio.get_event_loop()  # TODO switch to get_running_loop() in 3.7
        self._running = True
        self._next_timeout = self.io_loop.time()
        self._schedule_next()

    def stop(self) -> None:
        """Stops the timer."""
        self._running = False
        if self._timeout is not None:
            self._timeout.cancel()
            self._timeout = None

    def is_running(self) -> bool:
        """Returns ``True`` if this `._Poll` has been started.
        """
        return self._running

    def _run(self) -> None:
        if not self._running:
            return
        try:
            return self.callback()
        except Exception:
            logger.error("Exception in callback %r", self.callback, exc_info=True)
        finally:
            self._schedule_next()

    def _schedule_next(self) -> None:
        if self._running:
            self._update_next(self.io_loop.time())
            self._timeout = self.io_loop.call_at(self._next_timeout, self._run)

    def _update_next(self, current_time: float) -> None:
        interval_s = self.interval_ms / 1000.0
        if self._next_timeout <= current_time:
            # The period should be measured from the start of one call
            # to the start of the next. If one call takes too long,
            # skip cycles to get back to a multiple of the original
            # schedule.
            self._next_timeout += (math.floor((current_time - self._next_timeout) / interval_s) + 1) * interval_s
        else:
            # If the clock moved backwards, ensure we advance the next
            # timeout instead of recomputing the same value again.
            # This may result in long gaps between callbacks if the
            # clock jumps backwards by a lot, but the far more common
            # scenario is a small NTP adjustment that should just be
            # ignored.
            #
            # Note that on some systems if time.time() runs slower
            # than time.monotonic() (most common on windows), we
            # effectively experience a small backwards time jump on
            # every iteration because _Poll uses
            # time.time() while asyncio schedules callbacks using
            # time.monotonic().
            self._next_timeout += interval_s


def start(check_time: int = 500) -> None:
    """Begins watching source files for changes.
    """
    io_loop = asyncio.get_event_loop()
    if io_loop in _io_loops:
        return
    _io_loops[io_loop] = True
    if len(_io_loops) > 1:
        logger.warning("h2o_q.autoreload started more than once in the same process")
    modify_times = {}  # type: Dict[str, float]
    callback = functools.partial(_reload_on_update, modify_times)
    scheduler = _Poll(callback, check_time)
    scheduler.start()


def wait() -> None:
    """Wait for a watched file to change, then restart the process.

    Intended to be used at the end of scripts like unit test runners,
    to run the tests again after any source file changes (but see also
    the command-line interface in `main`)
    """
    io_loop = asyncio.get_event_loop()
    io_loop.call_soon(start)
    io_loop.run_forever()
    io_loop.close()


def watch(filename: str) -> None:
    """Add a file to the watch list.

    All imported modules are watched by default.
    """
    _watched_files.add(filename)


def add_reload_hook(fn: Callable[[], None]) -> None:
    """Add a function to be called before reloading the process.

    Note that for open file and socket handles it is generally
    preferable to set the ``FD_CLOEXEC`` flag (using `fcntl` or
    `os.set_inheritable`) instead of using a reload hook to close them.
    """
    _reload_hooks.append(fn)


def _reload_on_update(modify_times: Dict[str, float]) -> None:
    if _reload_attempted:
        # We already tried to reload and it didn't work, so don't try again.
        return
    # if process.task_id() is not None:
    #     # We're in a child process created by fork_processes.  If child
    #     # processes restarted themselves, they'd all restart and then
    #     # all call fork_processes again.
    #     return
    for module in list(sys.modules.values()):
        # Some modules play games with sys.modules (e.g. email/__init__.py
        # in the standard library), and occasionally this can cause strange
        # failures in getattr.  Just ignore anything that's not an ordinary
        # module.
        if not isinstance(module, types.ModuleType):
            continue
        path = getattr(module, "__file__", None)
        if not path:
            continue
        if path.endswith(".pyc") or path.endswith(".pyo"):
            path = path[:-1]
        _check_file(modify_times, path)
    for path in _watched_files:
        _check_file(modify_times, path)


def _check_file(modify_times: Dict[str, float], path: str) -> None:
    try:
        modified = os.stat(path).st_mtime
    except Exception:
        return
    if path not in modify_times:
        modify_times[path] = modified
        return
    if modify_times[path] != modified:
        logger.info("%s modified; restarting server", path)
        _reload()


def _reload() -> None:
    global _reload_attempted
    _reload_attempted = True
    for fn in _reload_hooks:
        fn()
    if hasattr(signal, "setitimer"):
        # Clear the alarm signal set by
        # ioloop.set_blocking_log_threshold so it doesn't fire
        # after the exec.
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
    # sys.path fixes: see comments at top of file.  If __main__.__spec__
    # exists, we were invoked with -m and the effective path is about to
    # change on re-exec.  Reconstruct the original command line to
    # ensure that the new process sees the same path we did.  If
    # __spec__ is not available (Python < 3.4), check instead if
    # sys.path[0] is an empty string and add the current directory to
    # $PYTHONPATH.
    if _autoreload_is_main:
        assert _original_argv is not None
        spec = _original_spec
        argv = _original_argv
    else:
        spec = getattr(sys.modules["__main__"], "__spec__", None)
        argv = sys.argv
    if spec:
        argv = ["-m", spec.name] + argv[1:]
    else:
        path_prefix = "." + os.pathsep
        if sys.path[0] == "" and not os.environ.get("PYTHONPATH", "").startswith(path_prefix):
            os.environ["PYTHONPATH"] = path_prefix + os.environ.get("PYTHONPATH", "")
    if not _has_execv:
        subprocess.Popen([sys.executable] + argv)
        os._exit(0)
    else:
        try:
            os.execv(sys.executable, [sys.executable] + argv)
        except OSError:
            # Mac OS X versions prior to 10.6 do not support execv in
            # a process that contains multiple threads.  Instead of
            # re-executing in the current process, start a new one
            # and cause the current process to exit.  This isn't
            # ideal since the new process is detached from the parent
            # terminal and thus cannot easily be killed with ctrl-C,
            # but it's better than not being able to autoreload at
            # all.
            # Unfortunately the errno returned in this case does not
            # appear to be consistent, so we can't easily check for
            # this error specifically.
            os.spawnv(
                os.P_NOWAIT, sys.executable, [sys.executable] + argv  # type: ignore
            )
            # At this point the event loop has been closed and finally
            # blocks will experience errors if we allow the stack to
            # unwind, so just exit uncleanly.
            os._exit(0)


_USAGE = """\
Usage:
  python -m h2o_q -m module.to.run [args...]
  python -m h2o_q path/to/script.py [args...]
"""


def main() -> None:
    """Command-line wrapper to re-run a script whenever its source changes.

    Scripts may be specified by filename or module name::

        python -m h2o_q -m h2o_q.test.runtests
        python -m h2o_q h2o_q/test/runtests.py

    Running a script with this wrapper is similar to calling
    `h2o_q.autoreload.wait` at the end of the script, but this wrapper
    can catch import-time problems like syntax errors that would otherwise
    prevent the script from reaching its call to `wait`.
    """
    # Remember that we were launched with autoreload as main.
    # The main module can be tricky; set the variables both in our globals
    # (which may be __main__) and the real importable version.

    import h2o_q.autoreload

    global _autoreload_is_main
    global _original_argv, _original_spec
    h2o_q.autoreload._autoreload_is_main = _autoreload_is_main = True
    original_argv = sys.argv
    h2o_q.autoreload._original_argv = _original_argv = original_argv
    original_spec = getattr(sys.modules["__main__"], "__spec__", None)
    h2o_q.autoreload._original_spec = _original_spec = original_spec
    sys.argv = sys.argv[:]
    if len(sys.argv) >= 3 and sys.argv[1] == "-m":
        mode = "module"
        module = sys.argv[2]
        del sys.argv[1:3]
    elif len(sys.argv) >= 2:
        mode = "script"
        script = sys.argv[1]
        sys.argv = sys.argv[1:]
    else:
        print(_USAGE, file=sys.stderr)
        sys.exit(1)

    try:
        if mode == "module":
            import runpy

            runpy.run_module(module, run_name="__main__", alter_sys=True)
        elif mode == "script":
            with open(script) as f:
                # Execute the script in our namespace instead of creating
                # a new one so that something that tries to import __main__
                # (e.g. the unittest module) will see names defined in the
                # script instead of just those defined in this module.
                global __file__
                __file__ = script
                # If __package__ is defined, imports may be incorrectly
                # interpreted as relative to this module.
                global __package__
                del __package__
                rerun(f.read(), globals(), globals())
    except SystemExit as e:
        logging.basicConfig()
        logger.info("Script exited with status %s", e.code)
    except Exception as e:
        logging.basicConfig()
        logger.warning("Script exited with uncaught exception", exc_info=True)
        # If an exception occurred at import time, the file with the error
        # never made it into sys.modules and so we won't know to watch it.
        # Just to make sure we've covered everything, walk the stack trace
        # from the exception and watch every file.
        for (filename, lineno, name, line) in traceback.extract_tb(sys.exc_info()[2]):
            watch(filename)
        if isinstance(e, SyntaxError):
            # SyntaxErrors are special:  their innermost stack frame is fake
            # so extract_tb won't see it and we have to get the filename
            # from the exception object.
            watch(e.filename)
    else:
        logging.basicConfig()
        logger.info("Script exited normally")
    # restore sys.argv so subsequent executions will include autoreload
    sys.argv = original_argv

    if mode == "module":
        # runpy did a fake import of the module as __main__, but now it's
        # no longer in sys.modules.  Figure out where it is and watch it.
        loader = pkgutil.get_loader(module)
        if loader is not None:
            watch(loader.get_filename())  # type: ignore

    wait()
