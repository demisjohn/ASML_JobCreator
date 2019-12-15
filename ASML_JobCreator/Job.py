"""
This file is part of the ASML_JobCreator package for Python 3.x.

version.py
    Contains only versioning info and strings/variables.
    ** Update this file when you increment the module version number. **
    Some of the strings in this file will be printed upon module import
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *            # global variables/methods to the module.
from .Cell import Cell             # Class Cell - Cell Structure options
from .Image import Image                    # Class Image 
from .Alignment import Alignment            # Class Alignment
from .Layer import Layer                    # class Layer


####################################################




class Job(object):
    '''
    Class for defining ASML Job file.
        
    Attributes
    ----------
    data : Data object
        Contains loaded data from file
    fits : list
        list of Fit objects, defining fitting regions and fiting data (losses, slopes etc.)
    
    TO DO: 
	- MyJob.check_cell( [C,R] ) - check if cell is on the wafer

    
    
    '''
    
    def __init__(self):
        '''Calls `self._buildfromdict(datadict)`. See `help(Trace)` for more info.'''
        self.Alignment = Alignment()    # Alignment object
        self.Cell = Cell()      # Cell object
        self.Image = Image      # Image constructor
        self.Layer = Layer      # Layer constructor
        
        """
        if kwargs:
            '''pop any required kwargs'''
            pass
            '''If there are unused key-word arguments'''
            ErrStr = "WARNING: Trace(): Unrecognized keywords provided: {"
            for k in kwargs.iterkeys():
                ErrStr += "'" + k + "', "
            ErrStr += "}.    Continuing..."
            print(ErrStr)
        """
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        str = ""
        str += "ASML_JobCreator.Job object:\n"
        
        return str
    #end __str__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Setters/Getters
    ##############################################
    def set_waveguide_length(self, length):
        '''Set the expected waveguide length. This is usually the length on your mask plate or measured fiber length.'''
        self.waveguide_length = length
    #end
    
    def get_waveguide_length(self):
        '''Return waveguide length.'''
        try:
            return self.waveguide_length
        except AttributeError:
            raise AttributeError("waveguide_length has not been set yet.  Use `set_waveguide_length()` or `scale_to_group_index()`.")
    #end
    
    
    
    
    ##############################################
    #       Plotting etc.
    ##############################################
    
    
    
    
    
    
  
#end class(Job)





################################################
################################################


