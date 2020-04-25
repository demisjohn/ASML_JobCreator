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

PM = Image( 
        ImageID="PM", 
        ReticleID="4544020*", 
        sizeXY=[1.640,1.640], 
        shiftXY=[0,0], 
        )


def get_Image():
    '''User calls this to get the Image object defined in this file. Returns the same object each time it's called (not a new copy).'''
    return PM
#end get_Image()
