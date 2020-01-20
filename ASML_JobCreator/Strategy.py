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
from .Mark import Mark as __Mark      # Mark class


####################################################




class Strategy(object):
    """
    Class for defining Alignment Strategy.
    
    
    Attributes
    ----------
        Job : The parent Job object, that this Alignment belongs to.
        
    """
    
    def __init__(self, ID, marks=None, parent=None):
        '''
        Parameters
        ----------
        ID : string
            Name of the strategy
        
        marks : iterable
            Iterable containing Mark objects to add to this strategy.
        
        parent : Alignment object
            The Alignment object this Strategy belongs to.
        '''
        self.parent = parent    # parent Alignment object
        self.MarkList = []
        if marks:
            for m in marks:
                self.add_mark( m )
        #end if(marks)
        
        self.parent.add_Strategy(self)
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Strategy object:\n"
        
        return s
    #end __str__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Setters/Getters
    ##############################################
    """
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
    """
    
    
    
    
    ##############################################
    #       General Functions
    ##############################################
    def add_mark ( self, marks, preference="preferred" ) :
        '''        
        Parameters
        ----------
        Marks : an iterable of Mark objects
            Pass the Mark objects to add to this Alignment Strategy. Accepts each Mark as 
            a single iterable containing Mark objects.
        
        preference : {"Backup", "Preferred"}, optional
            Should Mark(s) be added as prefferred or backup marks? Preferred is default.
            Synonyms for "preferred" include "p", not case-sensitive
            Synonyms for "backup" include "b", not case-sensitive
        '''
        for m in marks:
            if isinstance( m, __Mark ):
                self.MarkList.append( m )
            else:
                errstr = "Expected Mark object, instead got `%s` %s." %( str(m), str(type(m)) )
                raise ValueError(errstr)
    #end (add_mark)
    
    
    
    
    
  
#end class(Trace)





################################################
################################################


