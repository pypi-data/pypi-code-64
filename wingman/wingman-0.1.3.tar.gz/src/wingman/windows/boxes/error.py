"""
Copyright © 2016-2017, 2020 biqqles.

This file is part of Wingman.

Wingman is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Wingman is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Wingman.  If not, see <http://www.gnu.org/licenses/>.
"""
from PyQt5 import QtWidgets


class ReadError(QtWidgets.QMessageBox):
    """A message box notifying the user of a failure to read the game data."""
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setWindowTitle('Failed to read game data')
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.setText('Please check that you have configured Wingman to use a valid Discovery Freelancer installation.')
        self.addButton(QtWidgets.QPushButton('Configure paths'), QtWidgets.QMessageBox.AcceptRole)
        self.addButton(QtWidgets.QPushButton('Exit'), QtWidgets.QMessageBox.RejectRole)
