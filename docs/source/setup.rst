######
Setting Up Development Environment
######

The section describes how to set up environment for both frontend and backend development.

******************
Carla Installation
******************

System Requirements
===================
* Currently only support Windows or Linux.
* Graphics card with at least ``6GB`` memory.

Referenced from `quickstart - carla <https://carla.readthedocs.io/en/latest/start_quickstart/>`_.

Packaged Version
================
Download the pre-built packaged version from `this link
<https://github.com/carla-simulator/carla/blob/master/Docs/download.md>`_,
download Import additional assets Each release has its own additional package of
extra assets and maps. This additional package includes the maps Town06, Town07,
and Town10. These are stored separately to reduce the size of the build, so they
can only be imported after the main package has been installed.

1. `Download <https://github.com/carla-simulator/carla/blob/master/Docs/download.md>`_ the appropriate package for your desired version of CARLA.

2. Extract the package:
   * On Linux:
   move the package to the Import folder and run the following script to extract the contents::
     cd path/to/carla/root
     ./ImportAssets.sh

   * On Windows: Extract the contents directly in the root folder.

Build from Source
=================
+ See `building carla from source <https://carla.readthedocs.io/en/latest/build_carla/>`_ for general instruction.
+ `Docker scripts <https://github.com/UmichSIM/carla-docker-gui>`_ for installing carla on ANY Linux distribution.

********
Frontend
********
TODO

*******
Backend
*******

Windows-Specific Instructions
=============================
* Download python `here <https://www.python.org/downloads/windows/>`_. Note that currently only python3.8 is supported by the project.
* Install poetry `here <https://python-poetry.org/docs/#installation>`_.
* Clone this repository.
* Instead of normal ``poetry install``, need to ignore Linux-only packages::

   poetry install --only "main, dev"

* As an *Administrator*, set the `execution policy <https://stackoverflow.com/questions/4037939/powershell-says-execution-of-scripts-is-disabled-on-this-system>`_ by typing this into your PowerShell window::

   Set-ExecutionPolicy RemoteSigned

Linux/MacOS Specific Instruction
================================
* Clone and enter this repo.
* Install `pyenv <https://github.com/pyenv/pyenv>`_ and::

   pyenv install 3.8.13
   pyenv shell 3.8.13
   poetry env use $(which python)
   poetry install

General Instruction
===================
* Enter poetry environment::

   poetry shell

* Try any python file inside ``scripts`` folder::

   python scripts/pure_wizard.py
