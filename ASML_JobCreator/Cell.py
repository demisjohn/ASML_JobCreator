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
        
    """
    
    def __init__(self, parent=None):
        '''Creates empty object.'''
        self.Job = parent
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Cell object:\n"
        s += " Cell Size = " + str( self.get_CellSize() ) + " mm\n"
        s += " Cell Matrix Shift = " + str( self.get_MatrixShift() ) + " mm\n"
        s += " Die Per Cell = %s; Minimum for exposure = %i die\n" %( str( self.get_NumberDiePerCell() ), self.get_MinNumberDie() )
        s += " Edge Exclusion = %0.6f mm\n" % self.get_EdgeExclusion()
        s += " Round/Flat Clearance = %0.6f mm / %0.6f mm\n" % ( self.get_RoundEdgeClearance() , self.get_FlatEdgeClearance() )
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
            if WARN(): print("Using default values for `CellSize`.")
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
            if WARN(): print("Using default values for `MatrixShift`.")
            self.set_MatrixShift( Defaults.MATRIX_SHIFT )
            return self.MatrixShift
    #end
    
    
    def set_NumberDiePerCell(self, cellCR):
        '''Set number of internal Die exposed per Cell, as two-valued integer iterable. Eg. (1,1) or [3,3]'''
        try:
            self.NumberDiePerCell = [1,1]
            self.NumberDiePerCell[0] = cellCR[0]
            self.NumberDiePerCell[1] = cellCR[1]
        except IndexError:
            errstr = "Expected `cellCR` to be two-valued integer iterable. Eg. (1,1) or [3,3].  Instead got '%s'." % cellCR
            raise IndexError(errstr)
        #end try
    #end
    
    def get_NumberDiePerCell(self):
        '''Return Number of Die per Cell, as two-valued Col/Row list.'''
        try:
            return self.NumberDiePerCell
        except AttributeError:
            if WARN(): print("Using default values for `NumberDiePerCell`.")
            self.NumberDiePerCell =  Defaults.NUMBER_DIES
            return self.NumberDiePerCell
    #end
    
    
    def set_MinNumberDie(self, num):
        '''Set minimum number of internal Die that must fit on the wafer in order for Cell to get an exposure, as integer.'''
        try:
            self.MinNumberDie = int(num)
        except ValueError:
            errstr = "Expected `num`` to be a single integer.  Instead got '%s'." % num
            raise ValueError(errstr)
        #end try
    #end
    
    def get_MinNumberDie(self):
        '''Return Minimum Number of Die on the wafer to force exposure.'''
        try:
            return self.MinNumberDie
        except AttributeError:
            if WARN(): print("Using default values for `MinNumberDie`.")
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


