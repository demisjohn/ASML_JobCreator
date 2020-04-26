"""
This file is part of the ASML_JobCreator package for Python 3.x.

	/Images/PM.py - The "Primary Mark" alignment mark Image on an ASML reticle.
	
	<ImgName>.get_Image() : returns the Image object corresponding to the Image defined in this file.

- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2020

"""
####################################################
# Module setup etc.

#from ..__globals import *   # global variables/methods to the module.
from ..Image import Image   # import the Image class


####################################################
#       IMAGE DEFINITION
####################################################

SPM_Y = Image( 
        ImageID="SPM-Y", 
        ReticleID="4544020*", 
        sizeXY=[0.400000, 2.912000], 
        shiftXY=[11.680000, -11.680000], 
        )
# Note, ImageSize_X could actually be 0.28800mm, but non-identical masking is not implemented yet.


def get_Image():
    '''User calls this to get the Image object defined in this file. Returns the same object each time it's called (not a new copy).'''
    return SPM_Y
#end get_Image()
