"""
This file is part of the ASML_JobCreator package for Python 3.x.

Alignment.py
    Contains class 'Alignment', which imports classes 'Marks' and 'Strategy'.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *        # global variables/methods to the module.
from .Mark import Mark        # Alignment Marks class
from .Strategy import Strategy  # Alignment Strategy class

####################################################




class Alignment(object):
    """
    Class for ALignment info, containing Alignment Marks (Mark objects) and 
    Alignment Strategies (class Strategy).
    
    
    Attributes
    ----------
    data : Data object
        Contains loaded data from file
    fits : list
        list of Fit objects, defining fitting regions and fiting data (losses, slopes etc.)
        
    """
    
    def __init__(self, datadict, **kwargs):
        '''Create empty object, with pointers to the Mark and Strategy classes.'''
        self.Mark = Mark
        self.Alignment = Alignment
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        str = ""
        str += "OBR_Analysis.Trace object:\n"
        return str
    #end __str__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Classes
    ##############################################
    def add_Marks(self, *args):
        '''Takes any number of Marks objects as arguments.  Optionally a single iterable containing the Mark objects. Adds the passed Marks to the Job.'''
        return None
    #end
    
    
    
    
    
  
#end class(Alignment)





################################################
################################################


