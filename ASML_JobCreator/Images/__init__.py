"""
This file is part of the ASML_JobCreator package for Python 3.x.

/Images/*.py
    Each file inside the `Images/` subfolder will be imported as a predefined Image that users can call on.
    
	/MyImage.py - The filename defines the object name for this Image, in this case "MyImage".
		An Image object is instanciated, see help on the Image class for properties.
	
	The Image can be called via:
	    ASML_JobCreator.Images.MyImage.get_Image()

- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2020

"""
####################################################
# Module setup etc.

#from ..__globals import *   # global variables/methods to the module.


####################################################

# The following directs init to import all the files within it's directory that match *.py
#   from http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
import importlib    # functions for importing modules/packages

import os, sys
for module in os.listdir(os.path.dirname(__file__)):
    modbase, modext = os.path.splitext(  os.path.basename(module)  )
    if module == '__init__.py' or modext != '.py':
        continue
    #__import__(  module[:-3], locals(), globals()  )
    importlib.import_module(  "."+modbase, __name__ )

# remove imported utility functions from the module namespace
del module, modbase, modext, os, sys, importlib

