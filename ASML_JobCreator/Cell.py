"""
This file is part of the ASML_JobCreator package for Python 3.x.

Cell.py
    Contains class Cell, for setting Wafer Layout > Cell Structure properties.
    

- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Cell(object):
    """
    Class for defining Wafer Layout > Cell Structure
    
    Cell(  ):
        Creates empty object with default values.
    
    Methods
    -------
    set_CellSize( [x,y] )
        Required to be set by user.
        
	set_EdgeClearance( [x,y] )
	    Defaults to....

    set_EdgeExclusion( exc )
        Defaults to...

	¿ [w]afer cover

    set_DiePerCell( [x,y] )
        Defaults to 1 x 1.
        
    set_MinDiePerCell()
        Defaults to [1] die per cell.
        
    set_MatrixShift( [x,y] )
        Defaults to [0,0] default
    
    
    Attributes
    ----------
    x : integer
        Some Attribute

        
    """
    
    def __init__(self):
        '''Creates empty object.'''
        pass
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Cell object:\n"
        
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
    def set_CellSize(self, xy=[10,10] ):
        '''Set the Cell Size in millimeters, [x,y].'''
        if len(xy)==2: 
            self.CellSize = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_CellSize(self):
        '''Return Cell Size in mm, as two-valued list.'''
        try:
            return self.CellSize
        except AttributeError:
            if WARN(): warn("Using default values for `CellSize`.")
            self.set_CellSize( Defaults.CELL_SIZE)
            return self.CellSize
    #end
    
    def set_MatrixShift(self, xy=[0,0] ):
        '''Set the Cell Matrix Shift in millimeters, [x,y].'''
        if len(xy)==2: 
            self.MatrixShift = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_MatrixShift(self):
        '''Return Cell Matrix Shift in mm, as two-valued list.'''
        try:
            return self.MatrixShift
        except AttributeError:
            if WARN(): warn("Using default values for `MatrixShift`.")
            self.set_MatrixShift( Defaults.MATRIX_SHIFT )
            return self.MatrixShift
    #end
    
    
    def get_NumberDiePerCell(self):
        '''Return Number of Die per Cell, as two-valued Col/Row list.'''
        try:
            return self.NumberDiePerCell
        except AttributeError:
            if WARN(): warn("Using default values for `NumberDiePerCell`.")
            self.NumberDiePerCell =  Defaults.CELL_SIZE
            return self.NumberDiePerCell
    #end
    
    def get_MinNumberDie(self):
        '''Return Minimum Number of Die on the wafer to force exposure.'''
        try:
            return self.MinNumberDie
        except AttributeError:
            if WARN(): warn("Using default values for `MinNumberDie`.")
            self.MinNumberDie =  Defaults.MIN_NUMBER_DIES
            return self.MinNumberDie
    #end
    

    # - - - - - - - - - - - - - - - - - - - - - 
    # not user editable (yet):    
    def get_RoundEdgeClearance(self):
        '''Return Round Edge Clearance in mm.'''
        return Defaults.ROUND_EDGE_CLEARANCE
    #end
    
    def get_FlatEdgeClearance(self):
        '''Return Flat Edge Clearance in mm.'''
        return Defaults.FLAT_EDGE_CLEARANCE
    #end
    
    def get_EdgeExclusion(self):
        '''Return Edge Exclusion in mm.'''
        return Defaults.EDGE_EXCLUSION
    #end
    
    
    
    
    ##############################################
    #       Plotting etc.
    ##############################################
    
    
    
    
    
    
  
#end class(Cell)





################################################
################################################


