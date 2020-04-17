"""
This file is part of the ASML_JobCreator package, for Python 3.x.

globals.py
    Contains functions and variables that the entire module should have access to.
    
- - - - - - - - - - - - - - -

Demis D. John, 2018

"""

####################################################
# Module setup etc.

from .Defaults import Defaults              # Class Default
Defaults = Defaults()  # `Default` object

# - - - - - - - - - - - - - - - - - - - - - - - - - 

import numpy as np
#import matplotlib.pyplot as plt    # import this as-needed, not globally
from datetime import datetime      # better date/time handling

#from collections import OrderedDict as oDict    # Dictionary that maintains order

from warnings import warn       # for non-breaking warnings, warn("message")

#from scipy import constants as const    # speed of light, planks constant etc.
from scipy.constants import c   # 299792458 m/s
from scipy.constants import h
from scipy.constants import eV
from scipy.constants import pi

####################################################



global _DEBUG
_DEBUG = False   # set to true for verbose outputs onto Python console - applies to all submodules/files
# can be changed at run-time via `set/unset_DEBUG()`

global _WARN
_WARN = True      # globally set warning mode
# can be changed at run-time via `set/unset_WARN()`


#  These will override the value set above in `_DEBUG`
def set_DEBUG():
    '''Enable verbose output for debugging.'''
    global _DEBUG
    _DEBUG = True

def unset_DEBUG():
    '''Disable verbose debugging output.'''
    global _DEBUG
    _DEBUG = False

def DEBUG():
    '''Returns whether DEBUG is true or false.  
    Use to print debug-level messages, like so:
    >>> if DEBUG(): print('This function works')
    '''
    return _DEBUG


def set_WARN():
    '''Enable verbose output for debugging.'''
    global _WARN
    _WARN = True

def unset_WARN():
    '''Disable verbose debugging output.'''
    global _WARN
    _WARN = False

def WARN():
    '''Returns whether WARN is true or false.
    Use to print warn-level messages, like so:
    >>> if WARN(): print('This function works')'''
    return _WARN

#---------------------------------------#

# custom colormaps:
#from .colormap_HotCold import cm_hotcold

# Plot options
#PlotLabelFontSize = 16.0
#PlotLineWidth = 0.5     # ax.plot(... , linewidth=PlotLineWidth )



#---------------------------------------#

#if DEBUG(): print("Globals.py imported")