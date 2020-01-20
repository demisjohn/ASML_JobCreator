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
from .Mark import Mark          # Alignment Marks class
from .Strategy import Strategy  # Alignment Strategy class

####################################################




class Alignment(object):
    """
    Class for ALignment info, containing Alignment Marks (Mark objects) and 
    Alignment Strategies (class Strategy).
    
    
    Attributes
    ----------
    MarksList : List of Mark objects added to this Job/Alignment.
    StrategyList : List of Strategy objects added to this Job/Alignment.
    Job : The parent Job object, that this Alignment belongs to.
        
    """
    
    def __init__(self, parent=None):
        '''Create empty Alignment object, with pointers to the Mark and Strategy classes.'''
        self.parent = parent    # parent Job object
        self.MarkList = []
        self.StrategyList = []
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Alignment object:\n"
        for m in self.MarkList:
            s += str(m)
            s += " - - - - - - -"
        s+= "----------------"
        for a in self.StrategyList:
            s += str(s)
            s += " - - - - - - -"
        return s
    #end __str__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Classes
    ##############################################
    def Mark(self, MarkID, MarkType="PM", cell_index=None, cell_shift=None, wafer_coord=None):
        '''
        Mark(MarkID, MarkType="PM", cell_index=None, cell_shift=None, wafer_coord=None)
        
        Define an alignment mark, either by cell_index/cell_shift OR wafer_coord, not both.
        Returns a Mark object, calls Mark constructor.
        '''
        m = Mark(MarkID, MarkType, cell_index, cell_shift, wafer_coord, parent=self)
        #self.Job.add_marks ?
        return m
    #end Mark()
        
    
    
    def add_Marks(self, *args):
        '''Add the Marks to this job. Takes any number of Marks objects as arguments.  Optionally a single iterable containing the Mark objects. Adds the passed Marks to the Job.'''
        return None
    #end
    
    
    def Strategy(self, ID, marks=None):
        '''
        Define an alignment mark, either by cell_index/cell_shift OR wafer_coord, not both.
        Returns a Mark object, calls Mark constructor.
        '''
        m = Strategy(ID, marks, parent=self)
        #self.Job.add_marks ?  Make sure marks are in the Alignment?
        return m
    #end Mark()
    
    def add_Strategy(self, *strat):
        """
        Add Strategy objects to this Job.
    
        Parameters
        ----------
        *strat : Strategy objects
            Can pass Strategy objects each as it's own argument, or an array-like/iterable containing the Layer objects.  Order of the Layers will determine the order in the ASML job - first argument/item will be Strategy #1.
        """
        if len(strat) == 1 and np.iterable( strat[0] ):
            StrategyList = strat[0]
        else:
            StrategyList = strat
        #end if(images)
        
        for i,ii in enumerate(StrategyList):
            if isinstance(ii, strat):
                self.StrategyList.append( ii )
            else:
                raise ValueError( "Expected `Strategy` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(StrategyList)
    #end add_strategy()
    
    
    
    
  
#end class(Alignment)





################################################
################################################


