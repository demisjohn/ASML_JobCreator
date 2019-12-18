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
        
    Attributes
    ----------
    data : Data object
        Contains loaded data from file
    fits : list
        list of Fit objects, defining fitting regions and fiting data (losses, slopes etc.)
    
    TO DO: 
	- MyJob.check_cell( [C,R] ) - check if cell is on the wafer

    
    
    '''
    
    def __init__(self):
        '''Calls `self._buildfromdict(datadict)`. See `help(Trace)` for more info.'''
        self.Alignment = Alignment()    # Alignment object
        self.Cell = Cell()      # Cell object
        self.ImageList = []
        self.Layer = Layer      # Layer constructor
        self.LayerList = []
        
        """
        if kwargs:
            '''pop any required kwargs'''
            pass
            '''If there are unused key-word arguments'''
            ErrStr = "WARNING: Trace(): Unrecognized keywords provided: {"
            for k in kwargs.iterkeys():
                ErrStr += "'" + k + "', "
            ErrStr += "}.    Continuing..."
            print(ErrStr)
        """
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Job object:\n"
        s += " ======= Cell =======\n"
        s += str(self.Cell)
        s += " ====== Images ======\n"
        for i,ii in enumerate(self.ImageList):
            if i>0:    s += " - - - - - - - - -\n"
            s += str(ii)
        s += " ====== Layers ======\n"
        for i,ii in enumerate(self.LayerList):
            if i>0:    s += " - - - - - - - - -\n"
            s += str(i)
        s += " ==== Alignment =====\n"
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
    
    
    def add_images(self, *images):
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
    
    
  
#end class(Job)



################################################
################################################


