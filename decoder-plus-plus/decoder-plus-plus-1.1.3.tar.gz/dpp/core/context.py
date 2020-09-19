# vim: ts=8:sts=8:sw=8:noexpandtab
#
# This file is part of Decoder++
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QAction

from dpp.core.listener import Listener
from dpp.core.plugin import AbstractPlugin, Plugins
from dpp.core.shortcut import Shortcut, NullShortcut


class Context(QObject):
    """
    The context of the application.
    This includes often used functionality like logging, configuration and plugins.
    Interaction with this class should be limited to minimize dependencies.
    """

    shortcutUpdated = pyqtSignal('PyQt_PyObject')

    class Mode:
        """ A list of different application modes. """
        GRAPHICAL_UI = "gfx" # graphical user interface
        COMMAND_LINE = "cmd" # command shell
        INTERACTIVE = "interactive" # Python Interactive Shell

    class Shortcut:
        """ A set of all shortcut ids which can be used within the application. """

        FILE_EXIT = "file_exit"
        EDIT_CUT = "edit_cut"
        EDIT_COPY = "edit_copy"
        EDIT_PASTE = "edit_paste"
        OPEN_FILE = "open_file"
        SAVE_AS_FILE = "save_as_file"
        TAB_NEW = "tab_new"
        TAB_RENAME = "tab_rename"
        TAB_NEXT = "tab_next"
        TAB_PREVIOUS = "tab_previous"
        TAB_CLOSE = "tab_close"
        TAB_SELECT_ = "tab_select_{}"
        TAB_SELECT_1 = "tab_select_1"
        TAB_SELECT_2= "tab_select_2"
        TAB_SELECT_3 = "tab_select_3"
        TAB_SELECT_4 = "tab_select_4"
        TAB_SELECT_5 = "tab_select_5"
        TAB_SELECT_6 = "tab_select_6"
        TAB_SELECT_7 = "tab_select_7"
        TAB_SELECT_8 = "tab_select_8"
        TAB_SELECT_9 = "tab_select_9"
        FOCUS_CODEC_SEARCH = "focus_codec_search"
        FOCUS_ENCODER = "focus_encoder"
        FOCUS_DECODER = "focus_decoder"
        FOCUS_HASHER = "focus_hasher"
        FOCUS_SCRIPT = "focus_script"
        FOCUS_INPUT_TEXT = "focus_input_text"
        FOCUS_INPUT_TEXT_NEXT = "focus_input_text_next"
        FOCUS_INPUT_TEXT_PREVIOUS = "focus_input_text_previous"
        SELECT_PLAIN_VIEW = "select_plain_view"
        SELECT_HEX_DOCK = "select_hex_dock"
        SELECT_LOG_DOCK = "select_log_dock"
        TOGGLE_SEARCH_FIELD = "toggle_search_field"
        SHOW_PLUGINS = "show_plugins"

    def __init__(self, app_id, app_path, namespace):
        super(__class__, self).__init__()
        self._app_id = app_id
        self._app_path = app_path
        self._namespace = namespace
        self._logger = {}
        self.config = self._init_config()
        self._debug_mode = self.config.isDebugModeEnabled()
        self._listener = Listener(self)
        self._plugins = Plugins([
            os.path.join(self._app_path, "plugins"),
            os.path.join(str(Path.home()), ".config", "dpp", "plugins")], self)
        self._shortcuts = {}
        self._installed_packages = []
        self._mode = None

    def _init_config(self):
        """ Returns the configuration. """
        from dpp.core.config import Config
        return Config()

    def _init_logger(self, log_format):
        """ Returns the logger. """
        logger = logging.getLogger(self._app_id)
        log_level = logging.DEBUG if self.config.isDebugModeEnabled() else logging.WARN

        logging.root.setLevel(log_level)
        console_logger = logging.StreamHandler(sys.stderr)
        console_logger.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_logger)

        if log_level == logging.DEBUG:
            file_logger = logging.FileHandler(os.path.join(self.getAppPath(), "dpp.log"))
            file_logger.setLevel(log_level)
            file_logger_formatter = logging.Formatter(
                '%(asctime)s - %(module)s: %(lineno)d: %(msg)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
            file_logger.setFormatter(file_logger_formatter)
            logger.addHandler(file_logger)

        return logger

    def getAppName(self) -> str:
        """ Returns the name of the application. """
        return "Decoder++"

    def getAppVersion(self) -> str:
        """ Returns the version of the application. """
        return "1.0.0"

    def getAppPath(self):
        """ Returns the path where the main application is located. """
        return self._app_path

    def getAppID(self):
        """ Returns the ID of the application. """
        return self._app_id

    def setMode(self, mode: str):
        """ Sets the mode (see ``Context.Mode``) in which the application is currently running. """
        self._mode = mode

    def mode(self) -> str:
        """ :returns the mode (see ``Context.Mode``) the application is currently running in or None if unspecified. """
        return self._mode

    def setDebugMode(self, status: bool, temporary=False):
        """ Enables/Disables debug mode. """
        if not temporary:
            self.config.setDebugMode(status)
        self._debug_mode = status
        logging.root.setLevel(logging.DEBUG if status else logging.INFO)
        status_string = "enabled" if status else "disabled"
        self.logger().info("Debug Mode: {} {}".format(status_string, " (temporary) " if temporary else ""))

    def toggleDebugMode(self):
        """ Toggles the debug-mode on/off. """
        self.setDebugMode(not self.config.isDebugModeEnabled())

    def isDebugModeEnabled(self):
        """ Returns whether the debug mode is currently configured or temporary enabled. """
        return self.config.isDebugModeEnabled() or self._debug_mode

    def namespace(self):
        """
        Returns the namespace of the application to allow instances like the console to access classes and functions.
        """
        return self._namespace

    def listener(self) -> Listener:
        """ Returns the listener instance which allows to subscribe to certain events. """
        return self._listener

    def logger(self, log_format="%(module)s: %(lineno)d: %(msg)s", log_fields=None):
        """ Returns the logger of the application. """
        if log_format not in self._logger:
            self._logger[log_format] = self._init_logger(log_format)
        if log_fields:
            return logging.LoggerAdapter(self._logger[log_format], log_fields)
        return self._logger[log_format]

    def plugins(self) -> Plugins:
        """ Returns all plugins. """
        return self._plugins

    def checkDependency(self, package):
        """
        Checks whether the desired package is already installed.
        :param package: the package to check.
        :return: True, when the package is already installed, otherwise False.
        """
        if not self._installed_packages:
            # lazy initialize installed packages.
            reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
            self._installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        return package in self._installed_packages

    def registerShortcut(self, the_id: str, the_name: str, the_default_shortcut_key: str, the_callback, the_widget) -> QAction:
        """
        Registers a shortcut with the specified parameters.
        :param the_id: the id of the shortcut.
        :param the_name: the name of the shortcut which is displayed to the user.
        :param the_default_shortcut_key: the default shortcut key which may be overwritten by the user.
        :param the_callback: the callback which should be triggered when the shortcut is used.
        :param the_widget: the widget to which the shortcut is bound to.
        """
        the_shortcut_key = self.config.getShortcutKey(the_id)
        if not the_shortcut_key:
            the_shortcut_key = the_default_shortcut_key
        self.logger().debug("Registering shortcut {} to {}".format(the_id, the_shortcut_key))
        shortcut = Shortcut(the_id, the_name, the_shortcut_key, the_callback, the_widget)
        self._shortcuts[the_id] = shortcut
        self.config.setShortcutKey(the_id, the_shortcut_key)
        self.shortcutUpdated.emit(shortcut)
        return shortcut

    def updateShortcutKey(self, the_id: str, the_shortcut_key: str):
        """
        Updates the shortcut with the specified id.
        :param the_id: the id of the shortcut.
        :param the_shortcut_key: the shortcut key which should be used onwards.
        """
        if the_id not in self._shortcuts:
            self.logger().error("Shortcut {} is not defined".format(the_id))
            return

        self.logger().debug("Updating shortcut {} to {}".format(the_id, the_shortcut_key))
        shortcut = self._shortcuts[the_id]
        shortcut.setKey(the_shortcut_key)
        self.config.setShortcutKey(the_id, the_shortcut_key)
        self.shortcutUpdated.emit(shortcut)

    def getShortcuts(self) -> List[Shortcut]:
        """ Returns a list of shortcuts. """
        return self._shortcuts.values()

    def getShortcutById(self, the_id: str):
        """ Returns the shortcut with the specified id. """
        if the_id not in self._shortcuts:
            self.logger().error("Shortcut {} is not defined".format(the_id))
            return NullShortcut()
        return self._shortcuts[the_id]

    def getPluginByName(self, name: str, type: str) -> AbstractPlugin:
        return self.plugins().plugin(name, type)

    def saveAsFile(self, filename: str, content: str):
        with open(filename, "w") as f:
            f.write(content)

    def __deepcopy__(self, memo):
        """ There shall be only one. """
        return self
