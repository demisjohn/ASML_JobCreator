"""
This file is part of the ASML_JobCreator package for Python 3.x.

	/Images/SPM-X.py - The "Primary Mark" alignment mark Image on an ASML reticle.
	
    The Image Object's name must match the name of the file, or you will get an ImportError when importing ASML_JobCreator!  Make sure to use only valid characters, eg. no minus-signs or other punctuation, only underscores.  Also it is case-sensitive!

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

# Object name must exactly match the name of the file!
SPM_X = Image( 
        ImageID="SPM-X", 
        ReticleID="4544020*", 
        sizeXY=[2.912000/4, 0.408000/4], 
        shiftXY=[-11.680000/4, -11.680000/4], 
        )
# Note, ImageSize_Y could actually be 0.28800mm/4, but non-identical masking is not implemented yet.
