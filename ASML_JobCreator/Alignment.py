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
from .Mark import Mark as MarkClass # Alignment Marks class
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
    def Mark(self, MarkID, MarkType="PM", waferXY=None):
        '''Define a new alignment mark.
        Only waferXY (on-wafer coordinates) are implemented.
            
        Parameters
        ----------
        MarkID : string
            Name of the Mark
        
        MarkType : {"PM", "SPM_X", "SPM_Y" etc.}, optional
            Type of mark. Defaults to Primary Mark with both X/Y gratings, "PM".  See `help(Mark.set_marktype)` for full options.
        
        waferXY : two-valued iterable
            Wafer [X,Y] coordinates for this mark, relative to wafer center.
        
        Returns
        -------
        Returns the new Mark object, for later use in the Job.Alignment etc.
        
        ''' 
        return MarkClass(MarkID, MarkType, waferXY=waferXY, parent=self)
    #end Mark()
        
    
    
    def add_marks(self, *marks):
        """
        Add Mark objects to this Alignment object.
    
        Parameters
        ----------
        *marks : Mark objects
            Pass Mark objects, each as it's own argument. To pass an array-like/iterable containing the Mark objects, use star dereferencing.  
        """
        
        for i,ii in enumerate(marks):
            if isinstance(ii, MarkClass):
                self.MarkList.append( ii )
                ii.parent = self
            else:
                raise ValueError( "Expected `Mark` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(marks)
    #end
    
    
    def Strategy(self, ID, marks=None):
        '''
        Define an alignment mark, either by cell_index/cell_shift OR wafer_coord, not both.
        Returns a Mark object, calls Mark constructor.
        '''
        if not DEBUG():
            errstr = "This function is not fully implemented yet."
            raise NotImplementedError(errstr)
        #end if(DEBUG)
        
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


