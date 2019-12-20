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
    
    Layer( LayerID="", CombinedWithZeroLayer=False )
    
    Parameters
    ----------
    LayerID : string
        String identifying this Layer.
    CombinedWithZeroLayer : { True | False }, optional
        Whether this layer should also shoot alignment marks on Layer 0. Defaults to False.
        NOT IMPLEMENTED YET.
    parent : Job object
        The Job object that spawned this instance.
    
    """
    
    def __init__(self, LayerID="", CombinedWithZeroLayer=False, parent=None):
        '''Layer object constructor.  See `help(Layer)` for parameters.
        '''
        self.Job = parent
        self.LayerID = str(LayerID) # To Do: Sanitize LayerID text
        self.CombinedWithZeroLayer = bool(CombinedWithZeroLayer)
        self.ImageList = []
        self.EnergyList=[]
        self.FocusList=[]
        self.FocusTiltList=[]
        self.NAList=[]
        self.Sig_oList=[]
        self.Sig_iList=[]
        self.IlluminationModeList=[]
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Layer object:\n"
        s += "  Exposed Images:\n"
        for i in range( len(self.ImageList) ):
            s += "  %i: '%s'\n" % (i, self.ImageList[i].ImageID)
            s += "    Energy = %f mJ/cm^2\n" % self.EnergyList[i]
            s += "    Focus Offset = %0.3f mm\n" % self.FocusList[i]
            s += "    NA = %0.3f\n" % self.NAList[i]
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
    def set_CellSize(self, xy=[10,10] ):
        '''Set the Cell Size in millimeters, [x,y].'''
        if len(xy)==2: 
            self.CellSize = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_CellSize(self):
        '''Return Cell Size in mm, as two-valued list.'''
        try:
            return self.CellSize
        except AttributeError:
            if WARN(): warn("Using default values for `CellSize`.")
            self.set_CellSize( Defaults.CELL_SIZE)
            return self.CellSize
    #end
    
    
    ##############################################
    #       Alignment etc.
    ##############################################
    
    #########
    # To do
    #
    #set_strategy(Strat1) - or None
    #.set_Prealignment(Mark1, Mark2) - ignored if combined zero/first.
    #   also turns on optical prealignment
    #If any layer has "combined zero/first' set:
    #       MarksExposure - set layer 0 to expose all marks
    
    
    
    ##############################################
    #       Process Data
    ##############################################
    #
    # To DO:
    # .set/unset/get_shifted_measurement_scans()
    #
    
    
    def set_LayerShift(self, xy=[0,0] ):
        '''Set the Layer Shift in millimeters, [x,y].'''
        if len(xy)==2 and np.isscalar(xy[0]) and np.isscalar(xy[1]): 
            self.LayerShift = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_LayerShift(self):
        '''Return Layer Shift in mm, as two-valued list.'''
        try:
            return self.LayerShift
        except AttributeError:
            if WARN(): warn("Using default values for `LayerShift`.")
            self.set_LayerShift( Defaults.ProcessData_LAYER_SHIFT)
            return self.LayerShift
    #end
    
    def set_GlobalLevelPoints(self, xy1=[0,0], xy2=[0,0], xy3=[0,0] ):
        '''Set the Global Level/Tilt points in millimeters, [x,y].'''
        if len(xy1)==2 and np.isscalar(xy1[0]) and np.isscalar(xy1[1]): 
            self.GlobalLevel_Point1 = (xy1[0], xy1[1])
        else:
            raise ValueError("Expected x,y pair of numbers for `xy1`, instead got: " + str(xy1))
        #end if
        
        if len(xy2)==2 and np.isscalar(xy2[0]) and np.isscalar(xy2[1]): 
            self.GlobalLevel_Point2 = (xy2[0], xy2[1])
        else:
            raise ValueError("Expected x,y pair of numbers for `xy2`, instead got: " + str(xy2))
        #end if
        
        if len(xy3)==2 and np.isscalar(xy3[0]) and np.isscalar(xy3[1]): 
            self.GlobalLevel_Point3 = (xy3[0], xy3[1])
        else:
            raise ValueError("Expected x,y pair of numbers from `xy3`, instead got: " + str(xy3))
        #end if
    #end
    
    def get_GlobalLevelPoints(self):
        '''Return the three Global Level/Titl points in mm, as three two-valued tuples.'''
        try:
            return (self.GlobalLevel_Point1, self.GlobalLevel_Point2, self.GlobalLevel_Point3)
        except AttributeError:
            if WARN(): warn("Using default values for `GlobalLevel_Point1/2/3`.")
            self.set_GlobalLevelPoints(xy1=[0,0], xy2=[0,0], xy3=[0,0] )
            return (self.GlobalLevel_Point1, self.GlobalLevel_Point2, self.GlobalLevel_Point3)
    #end
    
    
    
    ##############################################
    #       Reticle Data
    ##############################################
    #
    # To DO:
    # 
    
    def expose_Image(self, Image=None, Energy=20, Focus=0.000, FocusTilt=[0,0], NA=0.570, Sig_o=0.750, Sig_i=0.5, IlluminationMode="Conventional"):
        """
        Set Layer to expose an Image.
    
        expose_Image( Image, Energy=20, Focus=0.000, FocusTilt=[0,0], NA=0.570, Sig_o=0.750, Sig_i=0.5, IlluminationMode="Conventional" )
    
        Parameters
        ----------
        Image : Image object
            Pass the Image object to expose.
        Energy : number
            Exposure energy in mJ.
        Focus : number
            The focus offset in mm.
        FocusTilt : two-valued array-like, optional
            Rx,Ry focus tilt values. Defaults to [0,0]
        NA : number, optional
            Numerical Aperture, defaults to 0.570
        Sig_o, Sig_i : numbers, optional
            Sigma Inner & Outer.  Defaul to Sig_o=0.750, Sig_i=0.5
        IlluminationMode : {"Conventional", "Annular"}
    
        """
        # TO DO: santize args
        self.ImageList.append( Image )
        self.EnergyList.append( Energy )
        self.FocusList.append( Focus )
        self.FocusTiltList.append( FocusTilt )
        self.NAList.append( NA )
        self.Sig_oList.append( Sig_o )
        self.Sig_iList.append( Sig_i )
        self.IlluminationModeList.append( IlluminationMode )
        
        ## NOT IMPLEMENTED:
        # add to the parent Job
        #self.Job.add_Layers(self)  # should check for duplicate Layers and check that Image is in the Job
    #end
    
    
  
#end class(Layer)





################################################
################################################


