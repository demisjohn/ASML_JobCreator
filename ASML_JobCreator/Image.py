"""
This file is part of the ASML_JobCreator package for Python 3.x.

Image.py
    defines the class Image.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Image(object):
    """
    Class Image, corresponding to Wafer layout > Image Definition & Image Distribution.
    
    Image( "ImageID", "ReticleID", [size_x, size_y], [shiftx,shifty] ):
        "ImageID" is...
        
    Methods
    -------
    Distribute(cell=[C,R], shift=[x,y])
	    shift is optional, defualts to [0,0]
        warn if shift >= cell size / 2
        (future) logic if Cell is outside wafer diam?     
    
    
    Attributes
    ----------
    data : Data object
        Contains loaded data from file
    fits : list
        list of Fit objects, defining fitting regions and fiting data (losses, slopes etc.)
        
    """
    
    def __init__(self, ImageID, ReticleID, sizeList, shiftList):
        '''Image object constructor.
        		__init__("ImageID", "ReticleID", [size_x, size_y], [shiftx,shifty])
		.Distribute(cell=[C,R], shift=[x,y])
			§ shift is optional, defualts to [0,0]
			§ warn if shift >= cell size / 2
			§ (future) logic if Cell is outside wafer diam?  

        '''
        
        
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
    
    
    
    
    
    
  
#end class(Image)




################################################
################################################


