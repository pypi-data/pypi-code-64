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

This file contains the application's entry point - main().
"""
import logging
import sys
import os

from PyQt5 import QtWidgets
import flint as fl

from wingman import app, config, IS_WIN  # non-relative imports for the benefit of PyInstaller
from wingman.windows.main.layout import MainWindow
from wingman.windows.boxes import configuration, loading, error


def main():
    """Main application entry point."""
    if not fl.paths.is_probably_freelancer(config.paths['freelancer_dir']):
        configuration.ConfigurePaths(mandatory=True).exec()

    fl.paths.set_install_path(config.paths['freelancer_dir'])
    if IS_WIN:
        import flair
        flair.set_install_path(config.paths['freelancer_dir'])

    # display a progress bar while the game files are loaded, and an error box if loading them fails
    try:
        loading.LoadingFiles().exec()
    except (TypeError, ValueError) as e:
        logging.error(f'Failed to read game data at {config.paths["freelancer_dir"]}', exc_info=e)
        # allow the user to configure paths again
        if error.ReadError().exec() == QtWidgets.QMessageBox.AcceptRole:
            main()
            return
        sys.exit(1)

    MainWindow()

    os._exit(app.exec())  # bad! but sys.exit isn't working after QApp start for some reason


if __name__ == '__main__':
    main()
