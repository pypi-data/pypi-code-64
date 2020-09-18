#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

import setuptools
from PIL import Image
from setuptools.command.build_py import build_py

NAME = "ciomaya"
DESCRIPTION = "Maya plugin for Conductor Cloud Rendering Platform."
URL = "https://github.com/AtomicConductor/conductor-maya"
EMAIL = "info@conductortech.com"
AUTHOR = "conductor"
REQUIRES_PYTHON = "~=2.7"
REQUIRED = ["ciocore>=0.2.10,<1.0.0"]
HERE = os.path.abspath(os.path.dirname(__file__))
DEV_VERSION = "dev.999"

with open(os.path.join(HERE, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

class BuildCommand(build_py):
    def run(self):
        build_py.run(self)
        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, NAME)
            self.write_version_info(target_dir)
            self.convert_icons(target_dir)

    def write_version_info(self, target_dir):

        for filename in [
            os.path.join(target_dir, "plug-ins", "Conductor.py"),
            os.path.join(target_dir, "conductor.mod"),
        ]:
            with open(filename, "r") as f:
                filedata = f.read()
            filedata = filedata.replace(DEV_VERSION, VERSION)
            with open(filename, "w") as f:
                f.write(filedata)

        with open(os.path.join(target_dir, "VERSION"), "w") as f:
            f.write(VERSION)


    def convert_icons(self, target_dir):
        out_icon_dir = os.path.join(target_dir, "icons")
        icons_dir = os.path.join("images", "icons")
        icon_files = os.listdir(icons_dir)
        for icon_file in icon_files:
            base, ext = os.path.splitext(icon_file)
            if not ext in [".png", ".jpg"]:
                continue
            icon_path = os.path.join(icons_dir, icon_file)
            for size in [36, 30, 24, 18]:
                icon = Image.open(icon_path)
                icon.thumbnail((size, size), Image.BICUBIC)
                out_icon_file = os.path.join(
                    out_icon_dir, "{}_{}x{}{}".format(base, size, size, ext))
                icon.save(out_icon_file)

        icons_dir = os.path.join("images", "nodeicons")
        icon_files = os.listdir(icons_dir)
        for icon_file in icon_files:
            base, ext = os.path.splitext(icon_file)
            if not ext in [".png", ".jpg"]:
                continue
            icon_path = os.path.join(icons_dir, icon_file)
            for size, prefix in [(36, ""), (18, "out_")]:
                icon = Image.open(icon_path)
                icon.thumbnail((size, size), Image.NEAREST)
                out_icon_file = os.path.join(
                    out_icon_dir, "{}{}{}".format(prefix, base, ext))
                icon.save(out_icon_file)


setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
    ],
    cmdclass={"build_py": BuildCommand},
    description=DESCRIPTION,
    install_requires=REQUIRED,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    include_package_data=True,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=VERSION,
    zip_safe=False,
    package_data={NAME: ["plug-ins/*.*", "icons/*.*",
                         "scripts/*.*", "conductor.mod"]}
)
