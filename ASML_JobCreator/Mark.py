"""
This file is part of the ASML_JobCreator package for Python 3.x.

Mark.py
    Class 'Mark', for defining alignment marks.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################


class Mark(object):
    """
    Class for defining alignment marks.
        
    Mark( MarkID, MarkType="PM", waferXY=[X,Y] )
    
    Parameters
    ----------
    LayerID : string
        String identifying this Alignment Mark.
    MarkType : { "PM" | "SPM_X" | "SPM_Y" }, optional
        Which type of alignment mark.
    parent : Job object
        The Job object that spawned this instance.  Only used internally.
        
    """
    
    def __init__(self, MarkID, MarkType="PM", waferXY=None, parent=None):
        '''Define an alignment mark, either by cell_index/cell_shift OR wafer-coord (not both).
        Only waferXY (on-wafer coordinates) are implemented.
            
        Parameters
        ----------
        MarkID : string
            Name of the Mark
        
        MarkType : {"PM", "SPM_X", "SPM_Y" etc.}, optional
            Type of mark. Defaults to Primary Mark with both X/Y gratings, "PM".  See `help(Mark.set_marktype)` for full options.
        
        waferXY : two-valued iterable
            Wafer [X,Y] coordinates for this mark, relative to wafer center.
        
        parent : Alignment object
            The Alignment object this Mark belongs to.
        
        '''
        from . import Images    # Image library from ./Images/
        self.Images = Images    
            
        self.parent = parent    # parent Alignment object
        self.set_MarkID(MarkID)
        self.set_marktype(MarkType)     # also sets self.Image
        
        self.waferXY = [0,0]
        self.waferXY[0] = float( waferXY[0] )
        self.waferXY[1] = float( waferXY[1] )
        
        self.isBackup = False
        
        self.parent.add_marks(self) # add this mark to the parent Alignment object
    #end __init__
    
    
    def __str__(self, tab=0):
        '''Return string to `print` this object. Indent the text with the `tab` argument, which will indent by the specified number of spaces (defaults to 0).'''
        s = ""
        s += " "*tab + "ASML_JobCreator.Mark object:\n"
        s += " "*tab + "  MarkID = '%s'\n" % self.MarkID
        s += " "*tab + "  MarkType = '%s'\n" % self.MarkType
        s += " "*tab + "  Wafer Location = (%0.6f, %0.6f) mm\n" %(self.waferXY[0], self.waferXY[1])
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
    
    def get_marktype(self):
        '''Return the type of alignment mark (PM, SPM etc.)'''
        return self.MarkType
    #end
    
    def set_marktype(self, MarkType_str):
        '''Set the type of Alignment Mark.
        
        Parameters
        ----------
        MarkType_str : string
            The string can have any of the following values (case inseitive).
            "PM" : Primary Mark, with both X and Y gratings. Dimensions 410 x 410 um
            "SPM-X" : Scribe-Line Primary Mark, X-oriented. Dimensions 728 x 72 um.
            "SPM-Y" : Scribe-Line Primary Mark, Y-oriented. Dimensions 72 x 728 um.
        
        Sets
        ----
        Mark.Image : Image object
            The Image corresponding to this Mark type, allowing for exposure of the Mark.  The Images are pre-defined in the ASML_JobCreator/Images/ folder.
        '''        
        s = str(MarkType_str).strip().lower()
        
        # argument synonym options:
        PM_Strings = ["pm","p"]
        SPM_X_Strings = ["spm_x","spmx","spm-x"]
        SPM_Y_Strings = ["spm_y","spmy","spm-y"]
        
        if np.any(  np.isin( PM_Strings , s )  ):
            out= 'pm'
            self.Image = self.Images.PM
        elif np.any(  np.isin( SPM_X_Strings , s )  ):
            out= 'spm_x'
            self.Image = self.Images.SPM_X
        elif np.any(  np.isin( SPM_Y_Strings , s )  ):
            out= 'spm_y'
            self.Image = self.Images.SPM_Y
        else:
            errstr = "Passed argument option `%s` is not in the list of valid options, which are:\n\t" + \
                str(PM_Strings) + "\n\t" + \
                str(SPM_X_Strings) + "\n\t" + \
                str(SPM_Y_Strings)
            raise ValueError(errstr)
        #end if
        
        self.Image.set_BaseImageID( self.Image.ImageID )
        self.MarkType = out
    #end set_marktype()
    
    
    
    def set_backup(self):
        '''Make this mark a "backup" mark, instead of preferred (the default).'''
        self.isBackup = True
    #end
    
    def unset_backup(self):
        '''Make this mark a "preferred" mark (the default), instead of "backup" mark.'''
        self.isBackup = False
    #end
    
    
    
    def get_MarkID(self):
        '''Return MarkID, as string.'''
        return self.MarkID
    
    def set_MarkID(self, MarkID):
        '''Set MarkID, as string.'''
        self.MarkID = str(MarkID)
    
    # aliases
    get_ID = get_MarkID
    set_ID = set_MarkID
    
#end class(Mark)





################################################
################################################


