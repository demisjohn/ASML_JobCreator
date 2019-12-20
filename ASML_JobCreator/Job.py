"""
This file is part of the ASML_JobCreator package for Python 3.x.

Job.py
    Contains the `Job` class, master class for defining an ASML Job.
    
    
- - - - - - - - - - - - - - -

TO DO: 
MyJob.check_cell( [C,R] ) - check if cell is on the wafer

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


####################################################




class Job(object):
    '''
    Class for defining ASML Job file.
        
    MyJob = Job( )
    
    
    TO DO: 
	- MyJob.check_cell( [C,R] ) - check if cell is on the wafer

    '''
    
    def __init__(self):
        '''Job object constructor.  See `help(Job)` for parameters.'''
        self.Alignment = Alignment()    # Alignment object
        self.Cell = Cell()      # Cell object
        self.ImageList = []
        self.LayerList = []
        
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Job object:\n"
        s += "======= Cell =======\n"
        s += str(self.Cell)
        s += "====== Images ======\n"
        for i,ii in enumerate(self.ImageList):
            if i>0:    s += " - - - - - - - - -\n"
            s += str(ii)
        s += "====== Layers ======\n"
        for i,ii in enumerate(self.LayerList):
            if i>0:    s += " - - - - - - - - -\n"
            s += str(ii)
        s += "==== Alignment =====\n"
        s += str(self.Alignment)
        
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
        '''Set the comment lines for this job, in three separate lines. Visible in PAS *Batch Append* screen.
        
        Parameters
        ----------
        line1, line2, line3 : string
            Maximum length = XYZ characters.  Only Sun-UNIX compatible characters!'''
        self.comment_line1 = str(line1)
        self.comment_line2 = str(line2)
        self.comment_line3 = str(line3)
    #end
    
    def get_comment(self):
        '''Return job comment lines, as three separate strings.'''
        try:
            return (self.comment_line1, self.comment_line2, self.comment_line3)
        except AttributeError:
            if WARN(): warn("Using default values for Job `comment`.")
            self.comment_line1, self.comment_line2, self.comment_line3 = \
                Defaults.comment_line1, Defaults.comment_line2, Defaults.comment_line3
            return (self.comment_line1, self.comment_line2, self.comment_line3) 
    #end
    
    
    def set_ExposeEdgeDie(self, tf):
        '''Enable/Disable the exposure of die all the way to the wafer edge, by setting the "Number of Die Per Cell" to 10x10, and Minimum Number of Die to 1.
        
        Parameters
        ----------
        tf : {True | False}
            Expose the edge die?
        '''
        if tf == True:
            self.Cell.NumberDiePerCell = [10, 10]
        else:
            self.Cell.NumberDiePerCell = [1, 1]
        #end if(b)
        self.Cell.MinNumberDie = 1
    #end
    
    
    
    # - - - - - - - - - - - - - - - - - - - - - 
    
    def get_WaferDiameter(self):
        '''Return Wafer Diameter in mm.'''
        return Defaults.WFR_DIAMETER
    #end
    
    
    ##############################################
    #       Adding Objects etc.
    ##############################################
    
    def Image(self, ImageID="", ReticleID="", sizeXY=[10,10], shiftXY=[0,0]):
        """
        Return Image object corresponding to Wafer layout > Image Definition & Image Distribution. After distributing the Image, make sure to add it into this Job with `Job.add_Images()``.
    
        Image( ImageID="MyImage", ReticleID="ReticleBarcode", sizeXY=[size_x, size_y], shiftXY=[shift_x, shift_y] )
    
        Parameters
        ----------
        JobObj : Job object
            The parent Job object that initiated this call.
        
        ImageID : string
            Your name for this Image.
        
        ReticleID : string
            The Barcode printed on the reticle.
        
        size_x, size_y : two-valued array-like
            Image Size in millimeters, passed as a single iterable (list, array, tuple) with two values. This should be the exact size of the Image extents on your reticle, not including the Image-Border region around it. eg. [10, 10]
        
        shift_x, shift_y : two-valued array-like
            Image Shift in millimeters, passed as a single iterable (list, array, tuple) with two values. This is the coordinate to the center of the Image, with respect to the center of the reticle. eg. [0, 0]
     
        """
        return Image(  ImageID=ImageID, ReticleID=ReticleID, sizeXY=sizeXY, shiftXY=shiftXY, parent=self)
    #end Image()
    
    
    def add_Images(self, *images):
        """
        Add Image objects to this Job.
    
        Parameters
        ----------
        *images : Image objects
            Can pass Image objects each as it's own argument, or an array-like/iterable containing the Image objects.  Order of the Images will determine the order in the ASML job - first argument/item will be Image #1.
        """
        if len(images) == 1 and np.iterable( images[0] ):
            ImgList = images[0]
        else:
            ImgList = images
        #end if(images)
        
        for i,ii in enumerate(ImgList):
            if isinstance(ii, Image):
                self.ImageList.append( ii )
            else:
                raise ValueError( "Expected `Image` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(ImgList)
    #end add_images()
    
    
    
    
    def Layer(self, LayerID="", CombinedWithZeroLayer=False):
        """
        Return a Layer object for this Job.
    
        Layer( LayerID="", CombinedWithZeroLayer=False )
    
        Parameters
        ----------
        LayerID : string
            String identifying this Layer.
        CombinedWithZeroLayer : { True | False }, optional
            Whether this layer should also shoot alignment marks on Layer 0. Defaults to False.
            NOT IMPLEMENTED YET.
    
        """
        return Layer( LayerID="", CombinedWithZeroLayer=False, parent=self)
    #end Layer()
    
    
    def add_Layers(self, *layers):
        """
        Add Layer objects to this Job.
    
        Parameters
        ----------
        *layers : Layer objects
            Can pass Layer objects each as it's own argument, or an array-like/iterable containing the Layer objects.  Order of the Layers will determine the order in the ASML job - first argument/item will be Layer #1.
        """
        if len(layers) == 1 and np.iterable( layers[0] ):
            LyrList = layers[0]
        else:
            LyrList = layers
        #end if(images)
        
        for i,ii in enumerate(LyrList):
            if isinstance(ii, Layer):
                self.LayerList.append( ii )
            else:
                raise ValueError( "Expected `Layer` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(LyrList)
    #end add_layers()
    
    def export(self, filepath=""):
        """
        Export an ASCII text file of this job, that can be imported by the ASML PAS software (with Job Creator software option installed).
    
        Parameters
        ----------
        filepath : string
            Path to save the text file to.  
        """
        s = self.__genascii()
        ascii = s.encode('ascii')
        with open(filepath, 'wb') as f:
            f.write(ascii)
        #end with file(filepath)
    #end export()
    
    
    def __genascii(self):
        """
        Return ASCII string for writing to a file, in ASML PAS compatible format. Pulls in all object data as defined by user.
        """
        tab = '   '
        col1 = 50       # Num Characters to offset column 1
        
        def indent(startstr='', spc = ' ', indent=col1):
            """Return string containing enough spaces so that any following text is indented `col1` characters, after `startstr`."""
            return spc * (  indent - len(startstr)  )
        #end indent()
        
        def add(string, cmd='', val='', tab=tab, cells=False):
            """Returns input `string` + `cmd` + `val` with the appropriate tab, indent and newlines."""
            s1 = tab + cmd
            if isinstance(val, str):
                s2 = indent(s1) + '"' + val + '"'
            elif np.size(val) == 2:
                if not cells:
                    s2 = indent(s1) + "%0.6f %0.6f" % tuple(val)
                else:
                    s2 = indent(s1) + '"%i" "%i"' % tuple(val)
                #end if(cells)
            else:
                s2 = indent(s1) + "%0.6f" % (val)
            #end if(str)
            return string + s1 + s2 + "\n"
        #end add()
        
        s = ''
        s += "\n\n"
        s += "START_SECTION GENERAL\n"
        
        """
        s1 = tab + "COMMENT"
        s2 = indent(s1) + self.get_comment()[0]
        s += s1 + s2
        
        s += indent() + self.get_comment()[1]
        s += indent() + self.get_comment()[2]
        """
        s = add(s, "COMMENT", self.get_comment()[0] )
        s = add(s, "", self.get_comment()[1] )
        s = add(s, "", self.get_comment()[2] )
        s = add(s, "MACHINE_TYPE", Defaults.MACHINE_TYPE)
        s = add(s, "RETICLE_SIZE", Defaults.RETICLE_SIZE)
        s = add(s, "WFR_DIAMETER", Defaults.WFR_DIAMETER)
        s = add(s, "WFR_NOTCH", Defaults.WFR_NOTCH)
        s = add(s, "CELL_SIZE", self.Cell.get_CellSize() )
        s = add(s, "ROUND_EDGE_CLEARANCE", self.Cell.get_RoundEdgeClearance() )
        s = add(s, "FLAT_EDGE_CLEARANCE", self.Cell.get_FlatEdgeClearance() )
        s = add(s, "EDGE_EXCLUSION", self.Cell.get_EdgeExclusion() )
        s = add(s, "COVER_MODE", Defaults.COVER_MODE)
        s = add(s, "NUMBER_DIES", self.Cell.get_NumberDiePerCell() )
        s = add(s, "MIN_NUMBER_DIES", self.Cell.get_MinNumberDie() )
        s = add(s, "PLACEMENT_MODE", Defaults.PLACEMENT_MODE)
        s = add(s, "MATRIX_SHIFT", self.Cell.get_MatrixShift())
        s = add(s, "PREALIGN_METHOD", Defaults.PREALIGN_METHOD)
        s = add(s, "WAFER_ROTATION", Defaults.WAFER_ROTATION)
        s = add(s, "COMBINE_ZERO_FIRST", Defaults.COMBINE_ZERO_FIRST)
        s = add(s, "MATCHING_SET_ID", Defaults.MATCHING_SET_ID)
        s += "END_SECTION\n"
        s += "\n\n\n\n\n"
        
        for I in self.ImageList:
            s += "START_SECTION IMAGE_DEFINITION\n"
            s = add(s, "IMAGE_ID", I.ImageID)
            s = add(s, "RETICLE_ID", I.ReticleID)
            s = add(s, "IMAGE_SIZE", I.sizeXY)
            s = add(s, "IMAGE_SHIFT", I.shiftXY)
            s = add(s, "MASK_SIZE", I.sizeXY)
            s = add(s, "MASK_SHIFT", I.shiftXY)
            s = add(s, "VARIANT_ID", Defaults.Image_VARIANT_ID)
            s += "END_SECTION\n"
            s += "\n\n\n\n\n"
            for D in I.get_distribution():
                s += "START_SECTION IMAGE_DISTRIBUTION\n"
                s = add(s, "IMAGE_ID", I.ImageID)
                s = add(s, "CELL_SELECTION", D[0], cells=True)
                s = add(s, "DISTRIBUTION_ACTION", Defaults.Image_DISTRIBUTION_ACTION)
                s = add(s, "OPTIMIZE_ROUTE", Defaults.Image_OPTIMIZE_ROUTE)
                s = add(s, "IMAGE_CELL_SHIFT", D[1])
                s += "END_SECTION\n"
                s += "\n"
            #end for(dist)
            s += "\n\n\n\n\n"
        #end for(ImageList)
                
        
        return s
    #end __genascii()
#end class(Job)



################################################
################################################


