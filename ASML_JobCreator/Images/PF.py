"""
This file is part of the ASML_JobCreator package for Python 3.x.

	/Images/PF.py - The "Flood Exposure" on top of PM alignment marks, on an ASML reticle.
	
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

PF = Image( 
        ImageID="PF", 
        ReticleID="4544020*", 
        sizeXY=[6.440000, 6.440000], 
        shiftXY=[10.560000, 0.000000], 
        )


def get_Image():
    '''User calls this to get the Image object defined in this file. Returns the same object each time it's called (not a new copy).'''
    return PF
#end get_Image()
