"""
This file is part of the ASML_JobCreator package.

Job.py
    Contains the `Job` class, master class for defining an ASML Job.
    Includes access functions for most critical Classes, functions, modules.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *            # global variables/methods to the module.
from .Cell import Cell              # Class Cell - Cell Structure options
from .Image import Image                    # Class Image 
from .Alignment import Alignment            # Class Alignment
from .Layer import Layer                    # Class Layer
from .Plot import Plot                      # Class Plot

####################################################




class Job(object):
    '''
    Class for defining ASML Job file.
        
    MyJob = Job( )
    
    Attributes
    ----------
    Cell : `Cell` object, containing Wafer Cell parameters.
    ImageList : List of Image objects added to this Job.
    LayerList : List of Layer objects added to this Job. Layers will utilize the Image objects in the ImageList.
    Alignment : Alignment object that contains Alignment Marks & Alignment Strategies.
    
    - - - - - - - 
    TO DO: 
	- MyJob.check_cell( [C,R] ) - check if cell is on the wafer
    - MyJob.CellCRtoWaferXY / WaferXYtoCellCR   - convert between cell and wafer coords.
    '''
    
    def __init__(self):
        '''Job object constructor.  See `help(Job)` for parameters.'''
        self.Alignment = Alignment(parent=self)    # Alignment object
        self.Cell = Cell(parent=self)      # Cell object
        self.ImageList = []
        self.LayerList = []
        self.defaults = Defaults    # imported in .__globals
        self.Plot = Plot(parent=self)
        
    #end __init__
    
    
    def __str__(self, tab=0):
        '''Return string to `print` this object. Indent the text with the `tab` argument, which will indent by the specified number of spaces (defaults to 0).'''
        s = ""
        s += " "*tab + "ASML_JobCreator.Job object:\n"
        s += " "*tab + "======= Cell =======\n"
        s += " "*tab + self.Cell.__str__(tab=1+tab)
        s += " "*tab + "====== Images ======\n"
        for i,I in enumerate(self.ImageList):
            if i>0:    s += " "*tab + " - - - - - - - - -\n"
            s += " "*tab + I.__str__(tab=1+tab)
        s += " "*tab + "====== Layers ======\n"
        for i,L in enumerate(self.LayerList):
            if i>0:    s += " "*tab + " - - - - - - - - -\n"
            s += " "*tab + L.__str__(tab=1+tab)
        s += " "*tab + "===== Alignment ====\n"
        s += " "*tab + self.Alignment.__str__(tab=1+tab)
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
    def set_comment(self, line1="", line2="", line3=""):
        '''Set the comment lines for this job, in three separate lines. These lines will be visible in PAS *Batch Append* screen.
        
        Parameters
        ----------
        line1, line2, line3 : string
            Maximum length = 50 characters.
        '''
        # replace non-ascii characters with '?', and ensure max 50 characters are kept:
        self.comment_line1 = str(line1).encode('ascii', errors='replace').decode()[0:50]
        self.comment_line2 = str(line2).encode('ascii', errors='replace').decode()[0:50]
        self.comment_line3 = str(line3).encode('ascii', errors='replace').decode()[0:50]
    #end
    
    def get_comment(self):
        '''Return job comment lines, as three separate strings.'''
        try:
            return (self.comment_line1, self.comment_line2, self.comment_line3)
        except AttributeError:
            if WARN(): print("Using default values for Job `comment`.")
            self.comment_line1, self.comment_line2, self.comment_line3 = \
                Defaults.comment_line1, Defaults.comment_line2, Defaults.comment_line3
            return (self.comment_line1, self.comment_line2, self.comment_line3) 
    #end
    
    
    def set_ExposeEdgeDie(self):
        '''
        Enable the exposure of die all the way to the wafer edge, by internally setting the "Number of Die Per Cell" to 50x50, and Minimum Number of Die to 1. See also `unset_ExposeEdgeDie()`. Variables being set are: `MyJob.Cell.NumberDiePerCell = [50,50]`, and `MyJob.Cell.NumberDiePerCell = 1`.
        '''
        self.Cell.NumberDiePerCell = [50, 50]
        self.Cell.MinNumberDie = 1
    #end
    
    def unset_ExposeEdgeDie(self):
        '''
        Disable the exposure of die all the way to the wafer edge, by internally setting the "Number of Die Per Cell" to 1x1, and Minimum Number of Die to 1.
        '''
        self.Cell.NumberDiePerCell = [1, 1]
        self.Cell.MinNumberDie = 1
    #end
    
    
    def get_WaferDiameter(self):
        '''Return Wafer Diameter in mm.'''
        return Defaults.WFR_DIAMETER
    #end
    
    
    def set_LensReduction(self, mag=4):
        '''Set the Lens Reduction/Magnifications as integer. Defaults to 4.  Corresponding `get_LensReduction()` function will return value from Defaults.py if unset by user.'''
        self.LensReduction = int(mag)
    #end
    
    def get_LensReduction(self):
        '''Return the Lens Reduction/Magnification.'''
        try:
            return self.LensReduction
        except AttributeError:
            self.LensReduction = Defaults.ProcessData_LENS_REDUCTION
            if WARN(): print(   "Using default values for Job `LensReduction` : %s" % (self.LensReduction)   )
            return self.LensReduction
    #end
    
    
    def set_CombinedZeroFirst(self):
        """Enable Combined Zero and First layer exposure. Unset (False) by default."""
        self.combined_zerofirst = True
    
    def unset_CombinedZeroFirst(self):
        """Disable Combined Zero and First layer exposure. This is the default state."""
        self.combined_zerofirst = False
    
    def get_CombinedZeroFirst(self):
        """Return True|False whether Combined Zero and First layer is enabled. Returns False if the parameter has not been set."""
        try: 
            return self.combined_zerofirst
        except AttributeError:
            self.combined_zerofirst = False
            return self.combined_zerofirst
        #end try
    #end getCombinedZeroFirst()
    
    
    ##############################################
    #       Adding Objects etc.
    ##############################################
    
    def Image(self, ImageID="", ReticleID="", sizeXY=[10,10], shiftXY=[0,0]):
        """
        Return Image object corresponding to Wafer layout > Image Definition & Image Distribution. After distributing the Image, make sure to add it into this Job with `Job.add_Images()``.
    
        Image( ImageID="MyImage", ReticleID="ReticleBarcode", sizeXY=[size_x, size_y], shiftXY=[shift_x, shift_y] )
    
        Parameters
        ----------
        ImageID : string
            Your name for this Image.
        
        ReticleID : string
            The Barcode printed on the reticle.
        
        size_x, size_y : two-valued array-like
            Image Size in millimeters, passed as a single iterable (list, array, tuple) with two values. This should be the exact size of the Image extents on your reticle, not including the Image-Border region around it. eg. [10, 10]
        
        shift_x, shift_y : two-valued array-like
            Image Shift in millimeters, passed as a single iterable (list, array, tuple) with two values. This is the coordinate to the center of the Image, with respect to the center of the reticle. eg. [0, 0]
     
        """
        if isinstance( ImageID, str):
            return Image(  ImageID=ImageID, ReticleID=ReticleID, sizeXY=sizeXY, shiftXY=shiftXY, parent=self)
        elif isinstance( ImageID, Image ):
            '''Was passed an Image object, probably from the /Images/ library.'''
            I = ImageID.copy()
            self.add_Images( I )
            return I
    #end Image()
    
    
    def add_Images(self, *images):
        """
        Add Image objects to this Job.
    
        Parameters
        ----------
        *images : Image objects
            Pass Image objects, each as it's own argument. To pass an array-like/iterable containing the Image objects, use star dereferencing.  Order of the Images will determine the order in the ASML job - first argument/item will be Image #1.
        """
        
        for i,I in enumerate(images):
            if isinstance(I, Image):
                if not np.isin( I, self.ImageList ):
                    if DEBUG(): print("Adding Image %s to ImageList" % I.__repr__()  )
                    self.ImageList.append( I )
                if I.parent and not (I.parent==self):
                    if WARN(): print(   "WARNING: Image objects can only be part of a single Job object.  Setting parent of Image `%s` to Job `%s`." %( I.ImageID, self.__repr__() )   )
                I.parent = self
            else:
                raise ValueError( "Expected `Image` object, instead got: " + str(type(I)) + " at argument #%i"%(i) )
        #end for(ImgList)
    #end add_images()
    
    
    
    
    def Layer(self, LayerID="", ZeroLayer=False, CombineWithZeroLayer=False):
        """
        Return a Layer object for this Job.
    
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
        return Layer( LayerID=LayerID, ZeroLayer=ZeroLayer, CombineWithZeroLayer=CombineWithZeroLayer, parent=self)
    #end Layer()
    
    
    def add_Layers(self, *layers):
        """
        Add Layer objects to this Job.
    
        Parameters
        ----------
        *layers : Layer objects
            Can pass Layer objects each as it's own argument. TO pass an array-like/iterable containing the Layer objects, use * dereferencing.  Order of the Layers will determine the order in the ASML job - first argument/item will be Layer #1.
        """
        
        for i,ii in enumerate(layers):
            if isinstance(ii, Layer):
                self.LayerList.append( ii )
            else:
                raise ValueError( "Expected `Layer` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(LyrList)
    #end add_layers()
    
    
    
    ##############################################
    #       Exporting to Text
    ##############################################
    
    def _organizeLayers(self):
        '''Reorganize the LayerList to account for any Layers that are set as `zero` layers, or have `combine with zero layer` enabled, which should be added to the job first and second, respectively.'''
        oldLL = self.LayerList.copy()   # avoid mutability
        newLL = []
        
        # Check for Zero layers
        zeros = [L.get_ZeroLayer() for L in oldLL]  # True/False list
        zeros_i = np.where(zeros)[0]    # index to ZeroLayers
        if DEBUG(): print("_organizeLayers(): zeros=", zeros, "zeros_i=", zeros_i)
        if len(zeros_i) > 1:
            errstr = "More than one Layer designated as `Zero` Layer!  The following Layers have ZeroLayer enabled:\n"
            errstr += str([  (L.LayerID +"\n") for L in [oldLL[i] for i in zeros_i]  ])
            raise ValueError(errstr)
        #end if multiple ZeroLayers
        
        if len(zeros_i):
            # add Zero to new Layer List, delete from old list
            if DEBUG(): print("Moving Zero layers...")
            newLL.append( oldLL[ zeros_i[0] ] )
            oldLL.pop( zeros_i[0] )
        
        # Check for Combo layers
        combos = [L.get_CombineWithZeroLayer() for L in oldLL]
        combos_i = np.where(combos)[0]    # index to ComboLayers
        if DEBUG(): print("_organizeLayers(): combos=", combos, "combos_i=", combos_i)
        if len(combos_i) > 1:
            errstr = "More than one Layer designated as `CombineWithZero` Layer!  The following Layers have CombineWithZeroLayer enabled:\n"
            errstr += str([  (L.LayerID +"\n") for L in [oldLL[i] for i in combos_i]  ])
            raise ValueError(errstr)
        #end if multiple CombosLayers
        
        if len(combos_i):
            # add ComboLyr to new Layer List, delete from old list
            if DEBUG(): print("Moving Combo layers...")
            newLL.append( oldLL[ combos_i[0] ] )
            oldLL.pop( combos_i[0] )
            self.set_CombinedZeroFirst()
        
        self.LayerList = newLL + oldLL
    #end _organizeLayers
    
    
    def export(self, filepath="ASML_Job.txt", overwrite=False):
        """
        Export an ASCII text file of this job, that can be imported by the ASML PAS software.

        Parameters
        ----------
        filepath : string
            Path to save the text file to.  
        
        overwrite : {True | False}, optional
            Whether to overwrite the file if it already exists.
            If asml.WARN() is enabled, will pop a warning before overwriting.
            Will fail with IOError if file exists and `overwrite` is False.
        """
        self._organizeLayers()  # check for Zero/CombinedWithZero options
        if DEBUG(): print( "Re-organized Layers:", [L.LayerID for L in self.LayerList] )
        
        import os.path
        from .exportlib import _genascii 
    
        s = _genascii(self)       # get the text to write
        ascii = s.encode('ascii')
    
        if os.path.exists(filepath):
            if (overwrite):
                if WARN(): print( "Overwriting output file at '%s'." %( os.path.abspath(filepath) ) )
            else:
                errstr = "File already exists at '%s' and argument `overwrite` is False." % ( os.path.abspath(filepath) )
                raise IOError(errstr)
            #end if(overwrite)
        #end if(exists(filepath))
    
        # open the file & write it:
        with open(filepath, 'wb') as f:
            if DEBUG(): print( "Opened file for writing at %s" %filepath)
            f.write(ascii)
        #end with file(filepath)
        if DEBUG(): print("Job.export(): ASCII Text file written succesfully.")
    #end export()
    
    ##############################################
    #       Utility Functions
    ##############################################
    
    def Wafer2Cell(self, WaferXY=[0.0, 0.0]):
        '''
        Return the CellCR pair [Col,Row] and ShiftXY ( [X,Y] offset from Cell Center) corresponding to the given WaferXY coordinate pair.
        
        Parameters
        ----------
        WaferXY : 2-valued list
            Wafer-coordinates as [X,Y]
        
        Returns
        -------
        CellCR : 2-valued iterable of integers
            Col,Row integers given in a 2-valued list, array, tuple etc.  Eg. [0,0] or [1,-2]
        ShiftXY : 2-valued iterable of floats
            X,Y shift from center of Cell, in a 2-valued list, array, tuple etc.
        '''
        return self.Cell.Wafer2Cell(WaferXY=WaferXY)
    
    
    def Cell2Wafer(self, CellCR=[0,0], ShiftXY=[0.0, 0.0]):
        '''
        Cell2Wafer(CellCR=[0,0], ShiftXY=[0.0, 0.0])
        
        Return the WaferXY coordinate pair corresponding to the CellCR [Col,Row] and ShiftXY ( [X,Y] offsets from Cell center).
        
        Parameters
        ----------
        CellCR : 2-valued iterable of integers
            Col,Row integers given in a 2-valued list, array, tuple etc.  Eg. [0,0] or [1,-2]
        ShiftXY : 2-valued iterable of floats
            X,Y shift from center of Cell, in a 2-valued list, array, tuple etc.
        
        Returns
        -------
        WaferXY : 2-valued list
            Wafer-coordinates as [X,Y]
        '''
        return self.Cell.Cell2Wafer(CellCR=CellCR, ShiftXY=ShiftXY)
    #end Cell2Wafer()
    
#end class(Job)



################################################
################################################


