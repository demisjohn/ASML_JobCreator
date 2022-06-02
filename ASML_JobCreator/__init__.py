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
    
    Conventions
    -----------
    All length units are specified in millimeters, and all coordinates are specified at 1x "wafer scale". Conversion with system magnification are done internally, including for reticle coordinates.
    Coordinates are in standard cartesian coordinates, with +X to the right and +Y up, assuming wafer-flat is down (negative Y).
    X/Y Coordinates should be passed in a two-valued array-like iterable, such as a two-valued [List], (Tuple), numpy array etc.  Eg. [10.1, -5.1] means 10.1mm in X and -5.1mm in Y.
    Similarly, Cell row/col "cellCR" selections should be passed as two-valued iterables of integers, such as `cellCR=[-1,1]`.
    
    ASML System Params
    ------------------
    The file `Defaults.py` includes system-hardware dependent parameters, such as wafer size, lens magnification, and other parameters that can be altered to make this module work with your ASML system.  Contact ASML or the maintainer of this package for help on setting up your Defaults.py file.  More more info, see `help(ASML_JobCreator.Defaults)` or `help(Job.defaults)`.
    

    __init__.py
        This is the main file that imports all other module files and functions.  
        Anything defined here is global to the module namespace.
        The parent folder name, "ASML_JobCreator", is the module name, and upon import, will run this file.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

@author: Demis D. John
"""

from .__version import version as __version__
from .__version import versiondate as __versiondate__
from .__version import author as __author__
print( "\nASML_JobCreator   (v."  +  __version__  +  "   "  +  __versiondate__ + ") + by " + __author__ + "\n")

####################################################
# Module setup etc.

from .__globals import * # global variables/methods to the module.
from .Job import Job      # objects for the ASML Job
from . import Images        # Predefined Image Library

####################################################
