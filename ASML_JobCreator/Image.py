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
    Class corresponding to Wafer layout > Image Definition & Image Distribution.   
    
    Image("ImageID", "ReticleID", [size_x, size_y], [shift_x, shift_y])
    
    Parameters
    ----------
    ImageID : string
        Your name for this Image.
        
    ReticleID : string
        The Barcode printed on the reticle.
        
    size_x, size_y : iterable of two numbers
        Image Size in millimeters, passed as a single iterable (list, array, tuple) with two values. This should be the exact size of the Image extents on your reticle, not including the Image-Border region around it.
        
    shift_x, shift_y : iterable of two numbers
        Image Shift in millimeters, passed as a single iterable (list, array, tuple) with two values. This is the coordinate to the center of the Image, with respect to the center of the reticle.
    
    To Do
    -----
    Distribute(cell=[C,R], shift=[x,y])
        § shift is optional, defualts to [0,0]
        § warn if shift >= cell size / 2
        § (future) logic if Cell is outside wafer diam?  
    """
    
    def __init__(self, ImageID, ReticleID, sizeList, shiftList):
        """
        Image object constructor.
        
        See `help(Image)` for description of arguments.
        """
        pass
        
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        str = ""
        str += "ASML_JobCreator.Image object:\n"
        
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
    #       Other methods
    ##############################################
    
    def Distribute(self, cell, shift):
        """
        Dist( Cell=[C,R], ImgShift=[x,y] )
            Cell : two-valued iterable of integers
                Which cell coordinate to distribute the Image object to.
            Shift :  two-valued iterable of floats, optional
                Image-to-Cell Shift. defaults to [0,0]
                warns if shift >= cell size / 2
                (future) logic if Cell is outside wafer diam?  
        """
        pass
    #end Distribute()
    
    
    
    
  
#end class(Image)




################################################
################################################


