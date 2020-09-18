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

from PyQt5 import QtCore, QtWidgets

from .pages import BasesPage, CommoditiesPage, FactionsPage, ShipsPage, GunsPage, ThrustersPage, ArmourPage, IDsPage, \
                    CountermeasuresPage, ShieldsPage, MinesPage, CloaksPage, EnginesPage
from ...widgets.infocardview import InfocardView
from ...widgets.scrollablelist import ScrollableList


class Database(QtWidgets.QDialog):
    """The Database dialogue provides a spreadsheet-esque window into every entity defined in Freelancer. It more or
    less replicates the functionality of FLStat, using flint as a backend."""
    title = f'Database'
    defaultDimensions = (1400, 800)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.resize(*self.defaultDimensions)
        self.setWindowFlags(QtCore.Qt.Window)

        self.pagesCache = {}

        self.mainLayout = QtWidgets.QHBoxLayout(self)

        viewSelector = ScrollableList(sorted(HEADINGS.keys()))
        viewSelector.setCurrentRow(1)
        viewSelector.currentTextChanged.connect(self.onSelectorChanged)
        self.mainLayout.addWidget(viewSelector, 0)

        self.infocardView = InfocardView(self)
        self.currentPage = BasesPage(self, self.infocardView)
        self.mainLayout.addWidget(self.currentPage, 4)
        self.mainLayout.addWidget(self.infocardView, 2)
        self.show()

    def onSelectorChanged(self, name):
        if HEADINGS[name] not in self.pagesCache:
            self.pagesCache[HEADINGS[name]] = HEADINGS[name](self, self.infocardView)
        newPage = self.pagesCache[HEADINGS[name]]

        self.currentPage.hide()
        self.mainLayout.replaceWidget(self.currentPage, newPage)
        self.currentPage = newPage
        self.currentPage.show()


HEADINGS = {
    'Bases': BasesPage,
    'Factions': FactionsPage,
    'Commodities': CommoditiesPage,
    'Ships': ShipsPage,
    'Indie IDs': IDsPage,
    'Guns': GunsPage,
    'Armour': ArmourPage,
    'Thrusters': ThrustersPage,
    'Mines': MinesPage,
    'CMs': CountermeasuresPage,
    'Shields': ShieldsPage,
    'Cloaks': CloaksPage,
    'Engines': EnginesPage,
}
