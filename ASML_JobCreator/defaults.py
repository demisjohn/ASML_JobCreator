"""
This file is part of the ASML_JobCreator package for Python 3.x.

defaults.py
    Contains & instantiates object of class Default, 
    containing hard-coded defualt values for many options.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Default(object):
    '''
    Class for holding all default values.
    '''
    
    def __init__(self):
        '''inits an empty object'''
    #end __init__
    
    
    """
    def __str__(self):
        '''Return string to `print` this object.'''
        str = ""
        str += "OBR_Analysis.Trace object:\n"
        
        return str
    #end __str__
    """
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
#end class(Default)



################################################
################################################

Defaults = Default()
Defaults.WaferDiam = 100    #mm


