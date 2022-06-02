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
        self.parent = parent    # parent Job object
        self.RoundEdgeClearance = Defaults.ROUND_EDGE_CLEARANCE
        self.FlatEdgeClearance = Defaults.FLAT_EDGE_CLEARANCE
        self.EdgeExclusion = Defaults.EDGE_EXCLUSION
    #end __init__
    
    
    def __str__(self, tab=0):
        '''Return string to `print` this object. Indent the text with the `tab` argument, which will indent by the specified number of spaces (defaults to 0).'''
        s = ""
        s += " "*tab + "ASML_JobCreator.Cell object:\n"
        s += " "*tab + " Cell Size = " + str( self.get_CellSize() ) + " mm\n"
        s += " "*tab + " Cell Matrix Shift = " + str( self.get_MatrixShift() ) + " mm\n"
        s += " "*tab + " Die Per Cell = %s; Minimum for exposure = %i die\n" %( str( self.get_NumberDiePerCell() ), self.get_MinNumberDie() )
        s += " "*tab + " Edge Exclusion = %0.6f mm\n" % self.get_EdgeExclusion()
        s += " "*tab + " Round/Flat Clearance = %0.6f mm / %0.6f mm\n" % ( self.get_RoundEdgeClearance() , self.get_FlatEdgeClearance() )
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
            if (xy[0] < Defaults.Cell_MinCellSize) or (xy[1] < Defaults.Cell_MinCellSize):
                raise ValueError( "Cell size [%f,%f]mm " %( xy[0], xy[1]) + "is too small, minimum is %f mm." % (Defaults.Cell_MinCellSize)  )
            self.CellSize = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_CellSize(self):
        '''Return Cell Size in mm, as two-valued list.'''
        try:
            return self.CellSize
        except AttributeError:
            if WARN(): print("Cell: Using default values for `CellSize`.")
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
            if WARN(): print("Cell: Using default values for `MatrixShift`.")
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
            if WARN(): print("Cell: Using default values for `NumberDiePerCell`.")
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
            if WARN(): print("Cell: Using default values for `MinNumberDie`.")
            self.MinNumberDie =  Defaults.MIN_NUMBER_DIES
            return self.MinNumberDie
    #end
    
    
    def set_RoundEdgeClearance(self, mm):
        '''Set Round Edge Clearance in mm.'''
        self.RoundEdgeClearance = float(mm)
    #end
    
    def get_RoundEdgeClearance(self):
        '''Return Round Edge Clearance in mm.'''
        return self.RoundEdgeClearance
    #end
    
    
    def set_FlatEdgeClearance(self, mm):
        '''Return Flat Edge Clearance in mm.'''
        self.FlatEdgeClearance = float(mm)
    #end
    
    def get_FlatEdgeClearance(self):
        '''Return Flat Edge Clearance in mm.'''
        return self.FlatEdgeClearance
    #end
    
    
    
    def set_EdgeExclusion(self, mm):
        '''Set Edge Exclusion in mm.'''
        self.EdgeExclusion = float(mm)
    #end
    
    def get_EdgeExclusion(self):
        '''Return Edge Exclusion in mm.'''
        return self.EdgeExclusion
    #end
    
    
    
    
    ##############################################
    #       Utility Functions
    ##############################################
    
    def Cell2Wafer(self, CellCR=[0,0], ShiftXY=[0.0, 0.0]):
        '''
        Cell2Wafer(CellCR=[0,0], ShiftXY=[0.0, 0.0])
        
        Return the WaferXY coordinate pair corresponding to the CellCR [Col,Row] and ShiftXY ( [X,Y] offsets from Cell center).
        
        Parameters
        ----------
        CellCR : 2-valued iterable of integers
            Col,Row integers given in a 2-valued list, array, tuple etc.  Eg. [0,0] or [1,-2]
        ShiftXY : 2-valued iterable of floats
            X,Y shift from center of Cell, in a 2-valued list, array, tuple etc.
        
        Returns
        -------
        WaferXY : 2-valued list
            Wafer-coordinates as [X,Y]
        '''
        ErrStr = "Cell: This function is not verified to work properly. Use `set_DEBUG()` to enable."
        if not DEBUG():
            raise NotImplementedError(ErrStr)
        else:
            if WARN(): print(ErrStr)
        
        X = self.get_MatrixShift()[0] + CellCR[0]*self.get_CellSize()[0] + ShiftXY[0]
        Y = self.get_MatrixShift()[1] + CellCR[1]*self.get_CellSize()[1] + ShiftXY[1]
        return [round(X,6), round(Y,6)]
    #end Cell2Wafer()
    
    
    def Wafer2Cell(self, WaferXY=[0.0, 0.0]):
        '''
        Return the CellCR pair [Col,Row] and ShiftXY ( [X,Y] offset from Cell Center) corresponding to the given WaferXY coordinate pair.
        
        Parameters
        ----------
        WaferXY : 2-valued list
            Wafer-coordinates as [X,Y]
        
        Returns
        -------
        CellCR : 2-valued iterable of integers
            Col,Row integers given in a 2-valued list, array, tuple etc.  Eg. [0,0] or [1,-2]
        ShiftXY : 2-valued iterable of floats
            X,Y shift from center of Cell, in a 2-valued list, array, tuple etc.
        '''
        ErrStr = "Cell: This function is not verified to work properly. Use `set_DEBUG()` to enable."
        if not DEBUG():
            raise NotImplementedError(ErrStr)
        else:
            if WARN(): print(ErrStr)
        
        from math import floor  # round down
        
        A = [0,0]
        CR = [0,0]
        XY = [0,0]
        
        A[0] = (WaferXY[0] - self.get_MatrixShift()[0]) 
        A[1] = (WaferXY[1] - self.get_MatrixShift()[1]) 
        
        if DEBUG(): print("Ax,Ay = ", A[0] , A[1])
        if DEBUG(): print("raw C,R = ", A[0] / self.get_CellSize()[0], A[1] / self.get_CellSize()[1]  )
        
        CR[0] = floor(  A[0] / self.get_CellSize()[0] )
        CR[1] = floor(  A[1] / self.get_CellSize()[1] )
        
        if DEBUG(): print("mod X,Y = ", 
            A[0] % self.get_CellSize()[0], 
            A[1] % self.get_CellSize()[1]
            )
        
        XY[0] = WaferXY[0] - CR[0]*self.get_CellSize()[0] + self.get_MatrixShift()[0] - self.get_CellSize()[0]/2
        XY[1] = WaferXY[1] - CR[1]*self.get_CellSize()[1] + self.get_MatrixShift()[1] - self.get_CellSize()[1]/2
        
        return [CR[0],CR[1]], [round(XY[0],6), round(XY[1],6)]
    #end Wafer2Cell()
    
    
    def get_ValidCells( self ):
        '''Return on-wafer Cells, for use in Image.distribute().
    
        Uses CellSize, MatrixShift, and RoundEdgeClearance.
        Accounts for FlatEdgeClearance (wafer flat exclusion), ExposeEdgeDie (shoot die that are partially on-wafer)
        Not yet able to be passed directly to Image.distribute(get_valid_cells()).  Currently must iterate through valid_cells and pass each [col,row] to Image.distribute().
        
        Parameters
        ----------
        none
    
        Returns
        -------
        valid_cells: a List of valid cell indices (indices are two-valued Lists of [col,row]).
    
        Contributed by Miguel Daal 2022, Ben Mazin group, U.California Santa Barbara, Physics Dept.'''
    
        #from numpy import floor, array, linalg.norm
        import numpy as np
    
        #find whole die
        cell_x, cell_y = self.get_CellSize()
        matrix_shift_x, matrix_shift_y = self.get_MatrixShift()
        wafer_diameter = self.parent.get_WaferDiameter() - 2*self.get_RoundEdgeClearance()
        wafer_flat_clearance = self.get_FlatEdgeClearance()
    
        max_num_cell_x = np.floor(wafer_diameter/cell_x)   
        max_num_cell_y = np.floor(wafer_diameter/cell_y)
    
        def get_cell_vertices(index_i, index_j):
                '''
                Given the  cell center point (center_x, center_y) and the matrix shift (matrix_shift_x, matrix_shift_y)
                return the four vertices of the cell as a list of numpy arrays in order: [UL, UR, LL, LR] (meaning "Upper/Lower + Left/Right").
                '''
                UL = np.array([cell_x/2,cell_y/2]) + np.array([index_i*cell_x, index_j*cell_y]) + np.array([matrix_shift_x, matrix_shift_y])
                UR = np.array([-cell_x/2, cell_y/2]) + np.array([index_i*cell_x, index_j*cell_y]) + np.array([matrix_shift_x, matrix_shift_y])
                LL = np.array([-cell_x/2, -cell_y/2]) + np.array([index_i*cell_x, index_j*cell_y]) + np.array([matrix_shift_x, matrix_shift_y])
                LR= np.array([cell_x/2, -cell_y/2]) + np.array([index_i*cell_x, index_j*cell_y]) + np.array([matrix_shift_x, matrix_shift_y])
                return [UL, UR, LL, LR]
        #end get_cell_vertices()
        
        def get_flat_edge_clearance_y():
            ''' return a y-coordinate representing the bottom wafer flat edge clearance - any point below this is invalid.'''
            F = Defaults.WFR_FLAT_LENGTH    # wafer flat length, mm
            D = Defaults.WFR_DIAMETER   # wafer diameter, mm
            Fc = F - self.get_FlatEdgeClearance()
            Dc = D - 2*self.get_RoundEdgeClearance()
            #Arc Angles:
            if Defaults.WFR_NOTCH.upper() == "N":
                Ac = np.rad2deg(  np.arcsin( (Fc/2) / (Dc/2) )  ) # arc angle corresponding to 1/2 of wafer flat clearance
            else:
                Ac = 2
            return -1 * np.cos( np.deg2rad(Ac) ) * (Dc/2)
        #end get_flat_edge_clearance_y()
        flat_edge_clearance_y = get_flat_edge_clearance_y()
        
        valid_cells = []
        cell_index_i = 0
        cell_index_j = 0
        cell_count_i = 0
        cell_count_j = 0
        sign_i = -1
        sign_j = -1
    
        while cell_index_i < max_num_cell_x+1:
            while cell_index_j < max_num_cell_y+1:
                vertices = get_cell_vertices(cell_index_i, cell_index_j)
                if self.parent.ExposeEdgeDie == False:
                    if not np.any(np.linalg.norm(vertices, axis = 1) > wafer_diameter/2):
                        if not np.any( [y for x,y in vertices] < flat_edge_clearance_y):
                            valid_cells.append([cell_index_i, cell_index_j])
                elif self.parent.ExposeEdgeDie == True:
                    if np.any( np.linalg.norm(vertices, axis = 1) <= wafer_diameter/2 ):
                        if np.any( [y for x,y in vertices] >= flat_edge_clearance_y ):
                            valid_cells.append([cell_index_i, cell_index_j])
                
                cell_count_j += 1
                sign_j *= -1
                cell_index_j = cell_index_j + cell_count_j * sign_j
            cell_count_i += 1
            sign_i *= -1
            cell_index_i = cell_index_i + cell_count_i * sign_i
            cell_index_j = 0
            cell_count_j = 0
            sign_j = -1
        #end while(cell_index)
    
        return  valid_cells 
    #end get_valid_cells()
    
    
    def is_ValidCell(self, cellCR):
        '''Return True/False whether specified Cell ([c,r] index) is valid for exposure.
        Uses get_ValidCells(), which accounts for Round/FlatEdgeClearance (wafer flat exclusion), ExposeEdgeDie (shoot die that are partially on-wafer).
        
        Parameters
        ----------
        cellCR : 2-valued iterable of integers
            Col,Row integers given in a 2-valued list, array, tuple etc.  Eg. [0,0] or [1,-2]
        
        Returns
        -------
        {True|False}: whether cell is valid for exposure/distribution.
        '''
        self.parent.check_CellCR(cellCR)
        
        try:
            self.get_ValidCells().index( cellCR )
            return True
        except ValueError:
            # cellCR was not found in get_ValidCells()
            return False
    #end is_ValidCell()
  
#end class(Cell)





################################################
################################################


