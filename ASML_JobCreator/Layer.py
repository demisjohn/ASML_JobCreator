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
        
    Parameters
    ----------
    LayerID : string
        String identifying this Layer.
        
    ZeroLayer : { True | False }, optional
        Whether this is a "Zero layer", meaning alignment marks only.  You should use `expose_marks()` for this layer.  This option is typically used along with another Layer that has `CombinedWithZeroLayer` enabled.
        
    CombinedWithZeroLayer : { True | False }, optional
        Whether this layer should also shoot alignment marks on Layer 0. Only one layer in your job can have this enabled. Defaults to False.
    parent : Job object
        The Job object that spawned this instance.
    
    """
    
    def __init__(self, LayerID="", ZeroLayer=False, CombineWithZeroLayer=False, parent=None):
        '''Layer object constructor.  See `help(Layer)` for parameters.
        '''
        self.parent = parent    # parent Job object
        self.LayerID = str(LayerID) # To Do: Sanitize LayerID text
        self.combined_zerofirst = bool(CombineWithZeroLayer)
        self.zero = bool(ZeroLayer)
        self.ImageList = []
        self.MarkList = []
        self.PreAlignMarksList = None
        self.GlobalStrategy = None
        
        # "Reticle Data" section:
        self.EnergyList=[]
        self.FocusList=[]
        self.FocusTiltList=[]
        self.NAList=[]
        self.Sig_oList=[]
        self.Sig_iList=[]
        self.IlluminationModeList=[]
        
        # add this Layer to the Job:
        self.parent.add_Layers( self )
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Layer object:\n"
        s += "  Layer ID = '%s'\n" % self.LayerID
        s += "  Exposed Images:\n"
        for i in range( len(self.ImageList) ):
            s += "  %i: '%s'\n" % (i, self.ImageList[i].ImageID)
            s += "    Energy = %f mJ/cm^2\n" % self.EnergyList[i]
            s += "    Focus Offset = %0.3f um\n" % self.FocusList[i]
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
    
    
    def set_combine_with_zero_layer(self):
        """
        Enable combination exposure of zero layer and first layer in one exposure session.  
        
        This requires that you enabled expose_marks() on the first Layer you defined (automatically numbered as "0"), and the next defined Layer will be automatically numbered as "1", which will be exposed at the same time.
        """
        self.combined_zerofirst = True
    #end 
    
    def unset_combine_with_zero_layer(self):
        """
        Disable combination exposure of zero layer and first layer in one exposure session.  
        """
        self.combined_zerofirst = False
    #end 
    
    def get_combine_with_zero_layer(self):
        """
        Return True|False for combination exposure of zero layer and first layer in one exposure session.  
        """
        return self.combined_zerofirst
    #end 
    
    
    
    def set_zero_layer(self):
        """
        Designated this Layer as a Zero layer.
        """
        self.zero = True
    #end
    
    def unset_zero_layer(self):
        """
        Un-Designated this Layer as a Zero layer.
        """
        self.zero = False
    #end
    
    def get_zero_layer(self):
        """
        Return True|False whether this Layer is designated as a Zero layer.
        """
        return self.zero
    #end
    
    
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
            if WARN(): print("Using default values for `LayerShift`.")
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
            if WARN(): print("Using default values for `GlobalLevel_Point1/2/3`.")
            self.set_GlobalLevelPoints(xy1=[0,0], xy2=[0,0], xy3=[0,0] )
            return (self.GlobalLevel_Point1, self.GlobalLevel_Point2, self.GlobalLevel_Point3)
    #end
    
    
    def _parse_IllumMode(self, mode ):
        '''
        Return santized string for Illumination Mode. Case insensitive.
        
        Available synonyms:
        - Default : ["default","d", "def"]
        - Conventional = ["conventional","c","conv"]
        - Annular = ["annular","a","ann"]
        '''
        s = str(mode).strip().lower()
        
        # argument synonym options:
        DefaultStr = ["default","d", "def"]
        ConvStr = ["conventional","c","conv"]
        AnnStr = ["annular","a","ann"]
        
        if np.any(  np.isin( DefaultStr , s )  ):
            out= 'Default'
        elif np.any(  np.isin( ConvStr , s )  ):
            out= 'Conventional'
        elif np.any(  np.isin( AnnStr , s )  ):
            out= 'Annular'
        else:
            errstr = "Passed argument option `%s` is not in the list of valid options,"%(mode) + " which are:\n\t" + \
                str(DefaultStr) + "\n\t" + \
                str(ConvStr) + "\n\t" + \
                str(AnnStr)
            raise ValueError(errstr)
        
        return out
    #end if
    
    
    def expose_Image(self, Image=None, Energy=20, Focus=0.000, FocusTilt=[0,0], NA=0.570, Sig_o=0.750, Sig_i=None, IlluminationMode="Default"):
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
        IlluminationMode : {"Default", "Conventional", "Annular"}, optional
            Defaults to "Default", which is whatever the machine default is, usually "Conventional".  See `help(_get_IllumMode)` for full list of accepted options for this parameter.
    
        """
        
        ## Santize args
        if np.isin( Image, self.ImageList ):
            raise ValueError(   "Image %s has already been added to this Layer %s."%( Image.__repr__, self.__repr__ )   )
        IlluminationMode = self._parse_IllumMode(IlluminationMode)
        
        ## Set the internal attributes
        self.ImageList.append( Image )
        self.EnergyList.append( Energy )
        self.FocusList.append( Focus )
        self.FocusTiltList.append( FocusTilt )
        self.NAList.append( NA )
        self.Sig_oList.append( Sig_o )
        self.Sig_iList.append( Sig_i )
        self.IlluminationModeList.append( IlluminationMode )
        
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
    
    def expose_Marks(self, Marks=[], Energy=20, Focus=0, FocusTilt=[0,0], NA=0.570, Sig_o=0.750, Sig_i=None, IlluminationMode="Default"):
        """
        Set Layer to expose some Alignment Marks.
    
        expose_Image( Image, Energy=20, Focus=0.000, FocusTilt=[0,0], NA=0.570, Sig_o=0.750, Sig_i=0.5, IlluminationMode="Conventional" )

        Parameters
        ----------
        marks : List of Mark objects
            Pass an iterable of Mark objects to expose.
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
        IlluminationMode : {"Default", "Conventional", "Annular"}, optional
            Defaults to "Default", which is whatever the machine default is, usually "Conventional"

        """
        for i,m in enumerate(Marks):
            ## Santize args
            IlluminationMode = self._parse_IllumMode(IlluminationMode)
                    
            ## Only add the Image once:
            if not np.isin( m.Image, self.ImageList ):
                self.ImageList.append( m.Image )
                self.EnergyList.append( Energy )
                self.FocusList.append( Focus )
                self.FocusTiltList.append( FocusTilt )
                self.NAList.append( NA )
                self.Sig_oList.append( Sig_o )
                self.Sig_iList.append( Sig_i )
                self.IlluminationModeList.append( IlluminationMode )
            #end if(Mark.Image not in ImageList)
            
            self.MarkList.append(m)
        #end for(Marks)
    #end expose_Marks()
    
    
    def set_PreAlignment(self,  mark1, mark2 ):
        """
        Enable Optical Prealignment on this Layer.
        Pass the two Mark objects corresponding to the alignment marks to be used for Optical Prealignment.
        
        Note that the chosen marks must lie in the limited region reachable by th eoptical prealignment camera system, and must be on opposide side of the wafer.
        """
        from .Mark import Mark as _Mark     # Mark class
        if isinstance(mark1, _Mark) and isinstance(mark2, _Mark):
            self.PreAlignMarksList = [mark1, mark2]
        else:
            errstr = "Expected exactly two Mark objects, instead got %s and %s."%(mark1.__repr__, mark2.__repr__)
            raise ValueError(errstr)
    #end set_PreAlignment()
    
    def unset_PreAlignment(self):
        """
        Disable Optical prealignment on this Layer.
        """
        self.PreAlignMarksList = None
    #end
    
    
    def set_GlobalAlignment(self,  strategy ):
        """
        Enable Global Alignment on this Layer.
        Pass the Alignment `Strategy` Object to be used for global alignment.
        """
        from .Alignment import Strategy as _Strategy    # class
        if isinstance(strategy, _Strategy):
            self.GlobalStrategy = strategy
        else:
            errstr = "Expected a Strategy object, instead got %s."%(strategy.__repr__)
            raise ValueError(errstr)
    #end set_GlobalAlignment()
    
    def unset_GlobalAlignment(self):
        """
        Disable Global Alignment strategy on this Layer.
        """
        self.GlobalStrategy = None
    #end
#end class(Layer)


################################################
################################################


