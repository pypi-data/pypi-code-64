# Dragonfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Dragonfly.
#
# Copyright (c) 2019, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Dragonfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
This component updates the Ladybug Tools core libraries and grasshopper components
to either the latest development version available (default) or to a specific
version of the grasshopper plugin.
_
The input version_ does not need to be newer than the current installation and can
be older but grasshopper plugin versions less than 0.3.0 are not supported.
A list of all versions of the Grasshopper plugin and corresponding release notes
can be found at: https://github.com/ladybug-tools/lbt-grasshopper/releases
_
This component can also overwrite the user libraries of standards (constructions,
schedules, modifiers) with a completely fresh copy if clean_standards_ is set to True.
-

    Args:
        _update: Set to True to update your installation of Ladybug Tools to the
            latest development version or to be at the version specified below.
        version_: An optional text string for the version of the grasshopper
            plugin which you would like to update to. The input should contain
            only integers separated by two periods (eg. 1.0.0). The version does
            not need to be newer than the current installation and can be older
            but grasshopper plugin versions less than 0.3.0 are not supported.
            A list of all versions of the Grasshopper plugin can be found
            here - https://github.com/ladybug-tools/lbt-grasshopper/releases
        clean_standards_: Set to True to have the library of standards (constructions,
            schedules, modifiers) overwritten with a completely fresh copy.
            DO NOT SET TO TRUE IF YOU WANT TO KEEP ANY OBJECTS THAT YOU HAVE
            ADDED TO YOUR honeybee_standards FOLDER. If False or None, any
            existing standards will be left alone.

    Returns:
        Vviiiiiz!: !!!
"""

ghenv.Component.Name = 'LB Versioner'
ghenv.Component.NickName = 'Versioner'
ghenv.Component.Message = '0.4.0'
ghenv.Component.Category = 'Ladybug'
ghenv.Component.SubCategory = '5 :: Version'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:
    from ladybug.futil import preparedir, nukedir, copy_file_tree, unzip_file
    from ladybug.config import folders
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:
    from ladybug_rhino.pythonpath import iron_python_search_path, create_python_package_dir
    from ladybug_rhino.download import download_file_by_name
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

import os
import subprocess
from Grasshopper.Folders import UserObjectFolders, DefaultAssemblyFolder


def get_python_exe():
    """Get the path to the Python installed in the ladybug_tools folder.

    Will be None if Python is not installed.
    """
    py_update = os.path.join(folders.ladybug_tools_folder, 'python')
    py_exe_file = os.path.join(py_update, 'python.exe') if os.name == 'nt' else \
        os.path.join(py_update, 'bin', 'python3')
    py_site_pack = os.path.join(py_update, 'Lib', 'site-packages') if os.name == 'nt' else \
        os.path.join(py_update, 'lib', 'python3.8', 'site-packages')
    if os.path.isfile(py_exe_file):
        return py_exe_file, py_site_pack
    return None, None


def get_recipe_directory():
    """Get the directory where Honeybee recipes are installed."""
    re_folder = os.path.join(folders.ladybug_tools_folder, 'resources', 'recipes')
    if not os.path.isdir(re_folder):
        os.makedirs(re_folder)
    return re_folder


def get_gem_directory():
    """Get the directory where measures distributed with Ladybug Tools are installed."""
    measure_folder = os.path.join(folders.ladybug_tools_folder, 'resources', 'measures')
    if not os.path.isdir(measure_folder):
        os.makedirs(measure_folder)
    return measure_folder


def get_standards_directory():
    """Get the directory where Honeybee standards are installed."""
    hb_folder = os.path.join(folders.ladybug_tools_folder, 'resources', 'standards')
    if not os.path.isdir(hb_folder):
        os.makedirs(hb_folder)
    return hb_folder


def remove_dist_info_files(directory):
    """Remove all of the PyPI .dist-info folders from a given directory.
    
    Args:
        directory: A directory containing .dist-info folders to delete.
    """
    for fold in os.listdir(directory):
        if fold.endswith('.dist-info'):
            nukedir(os.path.join(directory, fold), rmdir=True)


def update_libraries_pip(python_exe, package_name, version=None, target=None):
    """Change python libraries to be of a specific version using pip.

    Args:
        python_exe: The path to the Python executable to be used for installation.
        package_name: The name of the PyPI package to install.
        version: An optional string for the version of the package to install.
            If None, the library will be updated to the latest version with -U.
        target: An optional target directory into which the package will be installed.
        """
    # build up the command using the inputs
    if version is not None:
        package_name = '{}=={}'.format(package_name, version)
    cmds = [python_exe, '-m', 'pip', 'install', package_name]
    if version is None:
        cmds.append('-U')
    if target is not None:
        cmds.extend(['--target', target, '--upgrade'])

    # execute the command and print any errors
    print('Installing "{}" version via pip'.format(package_name))
    use_shell = True if os.name == 'nt' else False
    process = subprocess.Popen(
        cmds, shell=use_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()
    stdout, stderr = output
    return stderr


def download_repo_github(repo, target_directory, version=None):
    """Download a repo of a particular version from from github.

    Args:
        repo: The name of a repo to be downloaded (eg. 'lbt-grasshopper').
        target_directory: the directory where the library should be downloaded to.
        version: The version of the repository to download. If None, the most
            recent version will be downloaded. (Default: None)
        """
    # download files
    if version is None:
        url = "https://github.com/ladybug-tools/{}/archive/master.zip".format(repo)
    else:
        url = "https://github.com/ladybug-tools/{}/archive/v{}.zip".format(repo, version)
    zip_file = os.path.join(target_directory, '%s.zip' % repo)
    print 'Downloading "{}"  github repository to: {}'.format(repo, target_directory)
    download_file_by_name(url, target_directory, zip_file)

    #unzip the file
    unzip_file(zip_file, target_directory)

    # try to clean up the downloaded zip file
    try:
        os.remove(zip_file)
    except:
        print 'Failed to remove downloaded zip file: {}.'.format(zip_file)

    # return the directory where the unzipped files live
    if version is None:
        return os.path.join(target_directory, '{}-master'.format(repo))
    else:
        return os.path.join(target_directory, '{}-{}'.format(repo, version))


def parse_lbt_gh_versions(lbt_gh_folder):
    """Parse versions of compatible libs from a clone of the lbt-grasshopper repo.

    Args:
        lbt_gh_folder: Path to the clone of the lbt-grasshopper repo
 
    Returns:
        A dictionary of library versions formatted like so (but with actual version
        numbers in place of '0.0.0':

        {
            'lbt-dragonfly' = '0.0.0',
            'ladybug-rhino' = '0.0.0',
            'lbt-grasshopper' = '0.0.0',
            'honeybee-openstudio-gem' = '0.0.0',
            'honeybee-standards' = '0.0.0',
            'honeybee-energy-standards' = '0.0.0',
            'ladybug-grasshopper': '0.0.0',
            'honeybee-grasshopper-core': '0.0.0',
            'honeybee-grasshopper-radiance': '0.0.0',
            'honeybee-grasshopper-energy': '0.0.0',
            'dragonfly-grasshopper': '0.0.0',
            'ladybug-grasshopper-dotnet': '0.0.0'
        }
    """
    # set the names of the libraries to collect and the version dict
    version_dict = {
        'lbt-dragonfly': None,
        'queenbee-luigi': None,
        'ladybug-rhino': None,
        'honeybee-radiance-recipe': None,
        'honeybee-standards': None,
        'honeybee-energy-standards': None,
        'honeybee-openstudio-gem': None,
        'ladybug-grasshopper': None,
        'honeybee-grasshopper-core': None,
        'honeybee-grasshopper-radiance': None,
        'honeybee-grasshopper-energy': None,
        'dragonfly-grasshopper': None,
        'ladybug-grasshopper-dotnet': None
        }
    libs_to_collect = list(version_dict.keys())

    def search_versions(version_file):
        """Search for version numbers within a .txt file."""
        with open(version_file) as ver_file:
            for row in ver_file:
                try:
                    library, version = row.strip().split('==')
                    if library in libs_to_collect:
                        version_dict[library] = version
                except Exception :  # not a row with a ladybug tools library
                    pass

    # search files for versions
    requirements = os.path.join(lbt_gh_folder, 'requirements.txt')
    dev_requirements = os.path.join(lbt_gh_folder, 'dev-requirements.txt')
    ruby_requirements = os.path.join(lbt_gh_folder, 'ruby-requirements.txt')
    search_versions(requirements)
    search_versions(dev_requirements)
    search_versions(ruby_requirements)
    return version_dict


if all_required_inputs(ghenv.Component) and _update is True:
    # ensure that Python has been installed in the ladybug_tools folder
    py_exe, py_lib = get_python_exe()
    assert py_exe is not None, \
        'No Python instalation was found at: {}.\nThis is a requirement in ' \
        'order to contine with installation'.format(
            os.path.join(folders.ladybug_tools_folder, 'python'))

    # get the compatiable versions of all the dependencies
    temp_folder = os.path.join(folders.ladybug_tools_folder, 'temp')
    lbt_gh_folder = download_repo_github('lbt-grasshopper', temp_folder, version_)
    ver_dict = parse_lbt_gh_versions(lbt_gh_folder)
    ver_dict['lbt-grasshopper'] = version_

    # install the core libraries
    print 'Installing Ladybug Tools core Python libraries.'
    df_ver = ver_dict['lbt-dragonfly']
    stderr = update_libraries_pip(py_exe, 'lbt-dragonfly[cli]', df_ver)
    if os.path.isdir(os.path.join(py_lib, 'lbt_dragonfly-{}.dist-info'.format(df_ver))):
        print 'Ladybug Tools core Python libraries successfully installed!\n '
    else:
        give_warning(ghenv.Component, stderr)
        print stderr

    # install the queenbee core libraries
    print 'Installing Queenbee core Python libraries.'
    qb_ver = ver_dict['queenbee-luigi']
    stderr = update_libraries_pip(py_exe, 'queenbee-luigi[cli]', qb_ver)
    if os.path.isdir(os.path.join(py_lib, 'queenbee_luigi-{}.dist-info'.format(qb_ver))):
        print 'Queenbee core Python libraries successfully installed!\n '
    else:
        give_warning(stderr)
        print stderr

    # install the library needed for interaction with Rhino
    print 'Installing ladybug-rhino Python library.'
    rh_ver = ver_dict['ladybug-rhino']
    stderr = update_libraries_pip(py_exe, 'ladybug-rhino[cli]', rh_ver)
    if os.path.isdir(os.path.join(py_lib, 'ladybug_rhino-{}.dist-info'.format(rh_ver))):
        print 'Ladybug-rhino Python library successfully installed!\n '
    else:
        give_warning(ghenv.Component, stderr)
        print stderr
    if os.name != 'nt':  # make sure libraries are copied to the rhino scripts folder
        iron_python_search_path(create_python_package_dir())

    # install the grasshopper components
    print 'Installing Ladybug Tools Grasshopper components.'
    gh_ver = ver_dict['lbt-grasshopper']
    uo_folder = UserObjectFolders[0]
    stderr = update_libraries_pip(py_exe, 'lbt-grasshopper', gh_ver, uo_folder)
    lbgh_ver = ver_dict['ladybug-grasshopper']
    if os.path.isdir(os.path.join(uo_folder, 'ladybug_grasshopper-{}.dist-info'.format(lbgh_ver))):
        print 'Ladybug Tools Grasshopper components successfully installed!\n '
        remove_dist_info_files(uo_folder)  # remove the .dist-info files
    else:
        give_warning(ghenv.Component, stderr)
        print stderr

    # install the .gha Grasshopper components
    gha_folder = DefaultAssemblyFolder
    gha_location = os.path.join(gha_folder, 'ladybug_grasshopper_dotnet')
    if os.path.isdir(gha_location):
        msg = '.gha files already exist in your Components folder and cannot be ' \
            'deleted while Grasshopper is open.\nClose Grasshopper, delete the ' \
            '.gha files at\n{}\nand rerun this versioner component.\nOr simply keep '\
            'using the old .gha component if you do not need the latest ' \
            '.gha component features.\n '.format(gha_location)
        print msg
    else:
        gha_ver = ver_dict['ladybug-grasshopper-dotnet']
        stderr = update_libraries_pip(py_exe, 'ladybug-grasshopper-dotnet', gha_ver, gha_folder)
        package_dir = os.path.join(
            gha_folder, 'ladybug_grasshopper_dotnet-{}.dist-info'.format(gha_ver))
        if os.path.isdir(package_dir):
            print 'Ladybug Tools .gha Grasshopper components successfully installed!\n '
            remove_dist_info_files(gha_folder)  # remove the dist-info files
        else:
            give_warning(stderr)
            print stderr

    # install the honeybee_radiance_recipe package to recipe resources
    print 'Installing Honeybee recipes.'
    recipe_dir = get_recipe_directory()
    rec_ver = ver_dict['honeybee-radiance-recipe']
    if os.path.isdir(os.path.join(recipe_dir, 'honeybee_radiance_recipe')):
        nukedir(os.path.join(recipe_dir, 'honeybee_radiance_recipe'), True)
    stderr = update_libraries_pip(py_exe, 'honeybee-radiance-recipe', rec_ver, recipe_dir)
    if os.path.isdir(os.path.join(recipe_dir, 'honeybee_radiance_recipe-{}.dist-info'.format(rec_ver))):
        print 'Honeybee recipes successfully installed!\n '
        remove_dist_info_files(recipe_dir)  # remove the dist-info files
    else:
        give_warning(stderr)
        print stderr

    # install the honeybee-openstudio ruby gem
    gem_ver = ver_dict['honeybee-openstudio-gem']
    print 'Installing Honeybee-OpenStudio gem version {}.'.format(gem_ver)
    gem_dir = get_gem_directory()
    base_folder = download_repo_github('honeybee-openstudio-gem', gem_dir, gem_ver)
    source_folder = os.path.join(base_folder, 'lib')
    lib_folder = os.path.join(gem_dir, 'honeybee_openstudio_gem', 'lib')
    print 'Copying "honeybee_openstudio_gem" source code to {}\n '.format(lib_folder)
    copy_file_tree(source_folder, lib_folder)
    nukedir(base_folder, True)

    # always update the honeybee-energy-standards package
    print 'Installing Honeybee energy standards.'
    stand_dir = get_standards_directory()
    hes_ver = ver_dict['honeybee-energy-standards']
    if os.path.isdir(os.path.join(stand_dir, 'honeybee_energy_standards')):
        nukedir(os.path.join(stand_dir, 'honeybee_energy_standards'), True)
    stderr = update_libraries_pip(py_exe, 'honeybee-energy-standards', hes_ver, stand_dir)
    if os.path.isdir(os.path.join(stand_dir, 'honeybee_energy_standards-{}.dist-info'.format(hes_ver))):
        print 'Honeybee energy standards successfully installed!\n '
        remove_dist_info_files(stand_dir)  # remove the dist-info files
    else:
        give_warning(stderr)
        print stderr

    # install the standards libraries if requested or they don't exist
    if clean_standards_ or not os.path.isdir(os.path.join(stand_dir, 'honeybee_standards')):
        print 'Installing Ladybug Tools standards libraries (constructions, schedules, etc.).'
        hs_ver = ver_dict['honeybee-standards']
        if os.path.isdir(os.path.join(stand_dir, 'honeybee_standards')):
            nukedir(os.path.join(stand_dir, 'honeybee_standards'), True)
        stderr = update_libraries_pip(py_exe, 'honeybee-standards', hs_ver, stand_dir)
        if os.path.isdir(os.path.join(stand_dir, 'honeybee_standards-{}.dist-info'.format(hs_ver))):
            print 'Honeybee standards successfully installed!\n '
            remove_dist_info_files(stand_dir)  # remove the dist-info files
        else:
            give_warning(stderr)
            print stderr

    # delete the temp folder and give a completion message
    nukedir(temp_folder, True)
    print 'Update successful!'
    print 'Restart Grasshopper and Rhino to load the new components + library.'
else:  # give a message to the user about what to do
    print 'Make sure you are connected to the internet and set _update to True!'