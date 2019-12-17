"""
This file is part of the ASML_JobCreator package for Python 3.x.

Job.py
    Contains the `Job` class, master class for defining an ASML Job.
    
    
- - - - - - - - - - - - - - -

TO DO: 
MyJob.check_cell( [C,R] ) - check if cell is on the wafer

- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *            # global variables/methods to the module.
from .Cell import Cell              # Class Cell - Cell Structure options
from .Image import Image                    # Class Image 
from .Alignment import Alignment            # Class Alignment
from .Layer import Layer                    # Class Layer


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
        self.ImageList = []
        self.Layer = Layer      # Layer constructor
        self.LayerList = []
        
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
        str += "--- Cell ---\n"
        str += str(self.Cell)
        str += "--- Images ---\n"
        for i in self.ImageList:
            str += str(self.i)
        str += "--- Layers ---\n"
        for i in self.LayerList:
            str += str(self.i)
        str += "--- Alignment ---\n"
        str += str(self.Alignment)
        
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
    def set_comment(self, line1="", line2="", line3=""):
        '''Set the comment lines for this job, in three separate lines. Visible in PAS *Batch Append* screen.
        
        Parameters
        ----------
        line1, line2, line3 : string
            Maximum length = XYZ characters.  Only Sun-UNIX compatible characters!'''
        self.comment_line1 = str(line1)
        self.comment_line2 = str(line2)
        self.comment_line3 = str(line3)
    #end
    
    def get_comment(self):
        '''Return job comment lines, as three separate strings.'''
        try:
            return (self.comment_line1, self.comment_line2, self.comment_line3)
        except AttributeError:
            warn("Using default values for Job `comment`.")
            self.comment_line1, self.comment_line2, self.comment_line3 = \
                Defaults.comment_line1, Defaults.comment_line2, Defaults.comment_line3
            return (self.comment_line1, self.comment_line2, self.comment_line3) 
    #end
    
    
    def set_ExposeEdgeDie(self, b):
        '''Enable/Disable the exposure of die all the way to the wafer edge, by setting the "Number of Die Per Cell" to 10x10, and Minimum Number of Die to 1.
        
        Parameters
        ----------
        b : {True | False}
            Expose the edge die?
        '''
        if b == True:
            self.Cell.NumberDiePerCell = [10, 10]
        else:
            self.Cell.NumberDiePerCell = [1, 1]
        #end if(b)
        self.Cell.MinNumberDie = 1
    #end
    
    def get_NumberDiePerCell(self):
        '''Return Number of Die per Cell, as two-valued Col/Row list.'''
        try:
            return self.Cell.NumberDiePerCell
        except AttributeError:
            warn("Using default values for `NumberDiePerCell`.")
            self.Cell.NumberDiePerCell =  Defaults.CELL_SIZE
            return self.Cell.NumberDiePerCell
    #end
    
    def get_MinNumberDie(self):
        '''Return Minimum Number of Die on the wafer to force exposure.'''
        try:
            return self.Cell.MinNumberDie
        except AttributeError:
            warn("Using default values for `MinNumberDie`.")
            self.Cell.MinNumberDie =  Defaults.MIN_NUMBER_DIES
            return self.Cell.MinNumberDie
    #end
    
    
    # - - - - - - - - - - - - - - - - - - - - - 
    
    def get_WaferDiameter(self):
        '''Return Wafer Diameter in mm.'''
        return Defaults.WFR_DIAMETER
    #end
    
    
    ##############################################
    #       Plotting etc.
    ##############################################
    
    
    
    
    
    
  
#end class(Job)





################################################
################################################


