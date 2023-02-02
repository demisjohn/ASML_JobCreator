"""
This file is part of the ASML_JobCreator package for Python 3.x.

Layer.py
    Contains Layer class, which corresponds to the Layer Layout options.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.
from math import atan2, pi

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
        LayerID = str(LayerID).strip().upper()
        if len(LayerID) > 15:
            errstr = "Bad LayerID, {} : LayerID must be 15 characters or less.".format(LayerID)
            raise ValueError(errstr)
        LayerID_allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
        for c in LayerID:
            if c not in LayerID_allowed:
                errstr = "Bad LayerID, {} : character {} is not allowed.".format(LayerID, c)
                errstr += "\nAllowed characters: {}".format(LayerID_allowed)
                raise ValueError(errstr)
        self.LayerID = LayerID
        self.combined_zerofirst = bool(CombineWithZeroLayer)
        self.zero = bool(ZeroLayer)
        self.ImageList = []
        self.MarkList = []
        self.PreAlignMarksList = None
        self.GlobalStrategy = None
        self.SMS = False
        
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
    
    
    def __str__(self, tab=0):
        '''Return string to `print` this object. Indent the text with the `tab` argument, which will indent by the specified number of spaces (defaults to 0).'''
        s = ""
        s += " "*tab + "ASML_JobCreator.Layer object:\n"
        s += " "*tab + "  Layer ID = '%s'\n" % self.LayerID
        s += " "*tab + "  Zero Layer = %s\n" % (  str(self.get_ZeroLayer())  )
        s += " "*tab + "  CombineWithZero Layer = %s\n" % (  str(self.get_CombineWithZeroLayer())  )
        s += " "*tab + "  Exposed Images:\n"

        if bool( len(self.ImageList) ):
            for i in range( len(self.ImageList) ):
                s += " "*tab + "  %i: '%s'\n" % (i, self.ImageList[i].ImageID)
                s += " "*tab + "    Energy = %f mJ/cm^2\n" % self.EnergyList[i]
                s += " "*tab + "    Focus Offset = %0.3f um\n" % self.FocusList[i]
                s += " "*tab + "    Illuminationmode = `%s`\n" % self.IlluminationModeList[i]
                s += " "*tab + "    NA = %0.3f\n" % self.NAList[i]
                s += " "*tab + "    Sig_o = %0.3f\n" % self.Sig_oList[i]
                if self.Sig_iList[i]: s += " "*tab + "    Sig_i = %0.3f\n" % self.Sig_iList[i]
            #end for(ImageList)
        else:
            s += " "*tab + "    No Images exposed\n"
        #end if(Imagelist)
        
        s += " "*tab + "  Alignment Options:\n"
        if bool(  len(self.MarkList)  ):
            s += " "*tab + "  Exposed Alignment Marks:\n"
            for i in range( len(self.MarkList) ):
                s += " "*tab + self.MarkList[i].__str__(tab=2+tab)
                s += " "*tab + "    - - - - - -\n"
        else:
            s += " "*tab + "    No Marks exposed\n"
        #end if(MarkList)
        
        if bool(  self.PreAlignMarksList  ):
            s += " "*tab + "    Prealignment to Marks `%s` and `%s`\n" % (  self.PreAlignMarksList[0].get_MarkID(), self.PreAlignMarksList[1].get_MarkID()  )
        else:
            s += " "*tab + "    Prealignment disabled\n"
        
        if self.GlobalStrategy:
            s += " "*tab + "    Global Alignment Strategy: `%s`\n" % self.GlobalStrategy.get_ID()
        else:
            s += " "*tab + "    Global Alignment disabled\n"
        
        if self.SMS:
            s += " "*tab + "  Shifted Measurement Scans (SMS) Enabled\n"

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
    
    
    def set_CombineWithZeroLayer(self):
        """
        Enable combination exposure of zero layer and first layer in one exposure session.  
        
        This requires that you enabled expose_marks() on the first Layer you defined (automatically numbered as "0"), and the next defined Layer will be automatically numbered as "1", which will be exposed at the same time.
        """
        self.combined_zerofirst = True
    #end 
    
    def unset_CombineWithZeroLayer(self):
        """
        Disable combination exposure of zero layer and first layer in one exposure session.  
        """
        self.combined_zerofirst = False
    #end 
    
    def get_CombineWithZeroLayer(self):
        """
        Return True|False for combination exposure of zero layer and first layer in one exposure session.  
        """
        return self.combined_zerofirst
    #end 
    
    
    
    def set_ZeroLayer(self):
        """
        Designated this Layer as a Zero layer.
        """
        self.zero = True
    #end
    
    def unset_ZeroLayer(self):
        """
        Un-Designated this Layer as a Zero layer.
        """
        self.zero = False
    #end
    
    def get_ZeroLayer(self):
        """
        Return True|False whether this Layer is designated as a Zero layer.
        """
        return self.zero
    #end
    
    
    ##############################################
    #       Process Data Setters/Getters
    ##############################################    
    
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
    
    
    def set_ShiftedMeasurementScans(self):
        "Enable Shifted Measurement Scans (SMS) option, to increase Z/Tilt yield of edge die. This is a software option that must be licensed on your tool."
        self.SMS = True
    
    def unset_ShiftedMeasurementScans(self):
        "Disable Shifted Measurement Scans (SMS) option. This is the default state"
        self.SMS = False
    
    def get_ShiftedMeasurementScans(self):
        "Return {True|False} for whether Shifted Measurement Scans (SMS) option is enabled/disabled. Defaults to False."
        return self.SMS
    
    
    def get_LayerID(self):
        '''Return LayerID, if it has been set.  Otherwise, return `None`.'''
        return self.LayerID
    
    def set_LayerID(self, LayerID):
        '''Set LayerID as string.'''
        self.LayerID = str(LayerID)
    
    def unset_LayerID(self):
        '''Revert the LayerID back to default of "", allowing automatic choice during job creation.'''
        self.LayerID = ""
    
    # aliases
    get_ID = get_LayerID
    set_ID = set_LayerID
    
    ##############################################
    #       Exposures
    ##############################################  
    
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
            raise ValueError(   "Image `%s` has already been added to this Layer `%s`."%( Image.get_ID(), self.get_ID() )   )
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
        
        Image.Layers.append( self )
    #end
    
    
    ##############################################
    #       Alignment etc.
    ##############################################
    
    def expose_Marks(self, marks=[], Energy=20, Focus=0, FocusTilt=[0,0], NA=0.570, Sig_o=0.750, Sig_i=None, IlluminationMode="Default"):
        """
        Set Layer to expose some Alignment Marks.

        Parameters
        ----------
        marks : List of Mark objects
            Pass an iterable of Mark objects to expose.
        Energy : float
            Exposure energy in mJ.
        Focus : float, optional
            The focus offset in mm. Defaults to 0mm.
        FocusTilt : two-valued array-like, optional
            Rx,Ry focus tilt values. Defaults to [0,0]
        NA : number, optional
            Numerical Aperture, defaults to 0.570
        Sig_o, Sig_i : numbers, optional
            Sigma Inner & Outer.  Defaul to Sig_o=0.750, Sig_i=0.5
        IlluminationMode : {"Default", "Conventional", "Annular"}, optional
            Defaults to "Default", which is whatever the machine default is, usually "Conventional".

        """
        ## Santize args
        IlluminationMode = self._parse_IllumMode(IlluminationMode)
        
        for i,m in enumerate(marks):
            ## Only add the Image once:
            if DEBUG(): print("Layer.expose_marks(): not IsIn = ", not np.isin( m.Image, self.ImageList )  )
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
    
    
    def set_PreAlignment(self,  marks=[], check_position=False):
        """
        Enable Optical Prealignment on this Layer.
        Pass a list/iterable containing the two Mark objects corresponding to the alignment marks to be used for Optical Prealignment.
        
        Note that the chosen marks must lie in the limited region reachable by the optical prealignment camera system, and must be on opposide sides of the wafer.
        """
        from .Mark import Mark as _Mark     # Mark class
        
        try:
            mark1, mark2 = marks[0], marks[1]
        except IndexError:
            errstr = "Expected exactly two Mark objects, instead got: %s"%( marks )
            raise IndexError(errstr)

        # Ensure mark arguments were passed
        if isinstance(mark1, _Mark) and isinstance(mark2, _Mark):
            self.PreAlignMarksList = [mark1, mark2]
        else:
            errstr = "Expected exactly two Mark objects, "
            errstr += "instead got {} and {}.".format(
                mark1.__repr__(), mark2.__repr__() )
            raise ValueError(errstr)

        # check position requirements (possibly only for some ASML PAS systems)
        if check_position:
            # Ensure that marks are in allowed pre-alignment region
            # (See image in Issue 43)
            errtemplate = "\npre-alignment position {} ({:.6f},{:.6f}) not allowed"
            markallowed = [1, 1]
            errstr = ""
            r_min = 32.5 # mm (hard-coded, from image in Issue 43)
            r_max = Defaults.WFR_DIAMETER/2 - self.get_RoundEdgeClearance()
            # y_min = # TODO also forbid prealignment using flat clearance?
            # (see get_flat_edge_clearance_y in Cell.get_ValidCells)
            for ii, mark in enumerate([mark1, mark2]):
                x0, y0 = mark.waferXY
                d = 1.640/4 / 2 # half of the mark side-length
                for dx, dy in [(-d, -d), (d, -d), (-d, d), (d, d)] :
                    x1, y1 = x0+dx, y0+dy

                    theta = np.rad2deg(atan2(y1, x1))
                    if 20 <= theta <= 70: markallowed[ii] = 0; break
                    if 110 <= theta <= 160: markallowed[ii] = 0; break
                    if -70 <= theta <= -20: markallowed[ii] = 0; break
                    if -160 <= theta <= -110: markallowed[ii] = 0; break

                    r2 = x1*x1 + y1*y1
                    if r2 <= r_min*r_min: markallowed[ii] = 0; break
                    if r2 >= r_max*r_max: markallowed[ii] = 0; break
                    # TODO handle notch/wafer flat
                if not markallowed[ii]: errstr += errtemplate.format(ii+1, x0, y0)
            if errstr != "": raise ValueError(errstr)

            # Ensure that the marks on "opposite sides of the wafer"
            theta1 = np.rad2deg(atan2(mark1.waferXY[1], mark1.waferXY[0]))
            theta2 = np.rad2deg(atan2(mark2.waferXY[1], mark2.waferXY[0]))
            dtheta1 = abs(theta2 - theta1)
            dtheta2 = 360.0 - dtheta1
            dtheta = min([dtheta1, dtheta2])
            if dtheta <= 140.0 :
                errstr = "Expected marks on opposite sides of the wafer: "
                errstr += "mark angles are {:.1f} and {:.1f} degrees".format(
                    theta1, theta2)
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
        Pass the Alignment.Strategy Object to be used for global alignment.
        """
        from .Alignment import Strategy as _Strategy    # class
        if isinstance(strategy, _Strategy):
            self.GlobalStrategy = strategy
        else:
            errstr = "Expected a Strategy object, instead got %s."%(strategy.__repr__() )
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


