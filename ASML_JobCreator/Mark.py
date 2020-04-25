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
            Type of mark. Defaults to Primary Mark with both X/Y gratings, "PM".
        
        waferXY : two-valued iterable
            Wafer [X,Y] coordinates for this mark, relative to wafer center.
        
        parent : Alignment object
            The Alignment object this Mark belongs to.
        
        '''
        self.parent = parent    # parent Alignment object
        self.MarkID = str(MarkID)
        self.MarkType = self.__get_marktype(MarkType)
        
        self.waferXY = [0,0]
        self.waferXY[0] = float( waferXY[0] )
        self.waferXY[1] = float( waferXY[1] )
        
        self.parent.add_Marks(self) # add this mark to the parent Alignment object
    #end __init__
    
    
    def __get_marktype( s ):
        '''Analyze string argument `s` and Return sanitized strings for the Mark Type.'''
        s = str(s).strip().lower()
        
        # argument synonym options:
        PMStrings = ["pm","p"]
        SPM_X_Strings = ["spm_x","spmx"]
        SPM_Y_Strings = ["spm_y","spmy"]
        
        if np.any(  np.isin( PMStrings , s )  ):
            return 'pm'
        elif np.any(  np.isin( SPM_X_Strings , s )  ):
            return 'spm_x'
        elif np.any(  np.isin( SPM_Y_Strings , s )  ):
            return 'spm_y'
        else:
            errstr = "Passed argument option `%s` is not in the list of valid options, which are:\n\t" + \
                str(PMStrings) + "\n\t" + \
                str(SPM_X_Strings) + "\n\t" + \
                str(SPM_Y_Strings)
            raise ValueError(errstr)
        #end if
    #end get_marktype()
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Mark object:\n"
        s += "  MarkID = '%s'\n" % self.MarkID
        s += "  MarkType = '%s'\n" % self.MarkType
        s += "  Wafer Location = (%0.6f, %0.6f) mm\n" %(self.wafer_coord[0], self.wafer_coord[1])
        
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
    
    
    
    
    
    
  
#end class(Mark)





################################################
################################################


