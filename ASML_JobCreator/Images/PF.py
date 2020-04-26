"""
This file is part of the ASML_JobCreator package for Python 3.x.

	/Images/PF.py - The "Flood Exposure" on top of PM alignment marks, on an ASML reticle.
	
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
PF = Image( 
        ImageID="PF", 
        ReticleID="4544020*", 
        sizeXY=[6.440000/4, 6.440000/4], 
        shiftXY=[10.560000/4, 0.000000/4], 
        )
