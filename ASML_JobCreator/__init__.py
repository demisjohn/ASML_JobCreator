# -*- coding: utf-8 -*-
"""
ASML_JobCreator
    
    A python module to generate ASCII Job files for the ASML PAS 5500/300 stepper
    at the U.C. Santa Barbara Nanofabricaiton Facility. Only tested on this system,
    might work with other ASML systems with modifications.
    
    Description
    -----------
    This module provides a class and methods for defining Images, Wafer Layouts and 
    exposure jobs for an ASML Stepper.  It is intended to be used with the ASML
    software option "Job Creator", which allows for import of ASCII job files into
    the native binary format via the command `pas_recipe_import`.
    

    __init__.py
        The main file that imports all other module files and functions.  
        Anything defined here is global to the module namespace.
        The parent folder name, "ASML_JobCreator", is the module name, and upon import, will run this file.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

@author: Demis D. John
"""
# Define the sub-modules to import, that we want the user to use.
__all__ = ["data", "trace"]

from .__version import version as __version__
from .__version import versiondate as __versiondate__
from .__version import author as __author__
print( "\nASML_JobCreator   (v."  +  __version__  +  "   "  +  __versiondate__ + ") + by " + __author__ + "\n")

####################################################
# Module setup etc.

from .__globals import * # global variables/methods to the module.
from .Job import Job      # objects for the "Wafer Layout" section
from .defaults import Defaults


####################################################
# Function setup etc.

# Make data.open visible:
#from .data import open
