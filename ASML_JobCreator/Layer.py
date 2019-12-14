"""
This file is part of the ASML_JobCreator package for Python 3.x.

Layer.py
    Contains class Layer, which corresponds to the Layer Layout options.
    
    
	/Layer.py - class "Layer"
		__init__("LayerID", combinedwithZerolayer=True)
			- if true, then this layer should be added to file first, as layer #0.  should be no other layers with this option.  Defaults to False
		.set_strategy(Strat1) - or None
		.set_Prealignment(Mark1, Mark2) - ignored if combined zero/first.
				□ also turns on optical prealignment
		
		If any layer has "combined zero/first' set:
			MarksExposure - set layer 0 to expose all marks
		
		## Process_data:
		.set_shift( [x,y] )
			- less than Cell size / 2
		.set/unset/get_shifted_measurement_scans()
		## reticle data:
		.ExposeImage(Image1, Energy=, Focus=0, Focus_Tilt=[0,0], NA=0.57, Sig_o=0.750, Sig_i=, Illumination="Conventional")
		.set_GlobalLevelPoints( [x1,y1], [x2,y2], [x3,y3] )
		
		(Future-rev:)
		Layer1.un/set/get_ExposeMarks(Mark1,Mark2,Mark3 etc.) - accepts iterable
			- will also set "combined marks/image xposure" if marks are added
		


    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Layer(object):
    """
    Class for holding all Layer Layout options
    
    
    Attributes
    ----------
    data : Data object
        Contains loaded data from file
    fits : list
        list of Fit objects, defining fitting regions and fiting data (losses, slopes etc.)
        
    """
    
    def __init__(self, datadict, **kwargs):
        '''Empty object'''
        pass
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
    
    
    
    
    
    
  
#end class(Layer)





################################################
################################################


