"""
This file is part of the ASML_JobCreator package for Python 3.x.

Strategy.py
    Contains Alignment Strategy options in class 'Strategy'.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Strategy(object):
    """
    Class for defining Alignment Strategy.
    
    
    Attributes
    ----------
    data : Data object
        Contains loaded data from file
    fits : list
        list of Fit objects, defining fitting regions and fiting data (losses, slopes etc.)
        
    """
    
    def __init__(self, ID, marks):
        '''
        Parameters
        ----------
        ID : string
            Name of the strategy
        
        marks : iterable
            Iterable containing Mark objects to add to this strategy.
        '''
        pass
        #call self.add_mark() on each amrk passed.
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
	def add_mark ( self, preference="Backup"/"Preferred", *args ) 
		''''- accepts iterable for marks'''
		pass
	#end (add_mark)
    
    
    
    
    
  
#end class(Trace)





################################################
################################################


