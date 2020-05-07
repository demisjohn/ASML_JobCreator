"""
This file is part of the ASML_JobCreator package for Python 3.x.

Image.py
    defines the class Image.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################


class Image(object):
    """
    Class corresponding to Wafer layout > Image Definition & Image Distribution.   
    
    Image( ImageID="MyImage", ReticleID="ReticleBarcode", sizeXY=[size_x, size_y], shiftXY=[shift_x, shift_y], parent=JobObj )
    
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
    
    parent : Job object
        The Parent object that spawned this Image, containing relevant Cell parameters etc. 
    
    To Do
    -----
    Distribute(cell=[C,R], shift=[x,y])
        § shift is optional, defualts to [0,0]
        § warn if shift >= cell size / 2
        § (future) logic if Cell is outside wafer diam?  
    """
    
    def __init__(self, ImageID="", ReticleID="", sizeXY=[10,10], shiftXY=[0,0], parent=None):
        """
        Image object constructor.
        
        See `help(Image)` for description of arguments.
        """
        self.parent = parent    # parent Job object
        self.ImageID = str(ImageID)
        self.BaseImageID = None
        self.ReticleID = str(ReticleID)
        if len(sizeXY) == 2 and np.isscalar(sizeXY[0]) and np.isscalar(sizeXY[1]):
            self.sizeXY = (sizeXY[0], sizeXY[1])
        else:
            raise ValueError("Expected x,y pair of numbers for `sizeXY`, instead got: " + str(sizeXY))
        #end len(sizeXY)
        
        if len(shiftXY) == 2 and np.isscalar(shiftXY[0]) and np.isscalar(shiftXY[1]):
            self.shiftXY = (shiftXY[0], shiftXY[1])
        else:
            raise ValueError("Expected x,y pair of numbers for `shiftXY`, instead got: " + str(shiftXY))
        #end len(sizeXY)
        
        self.Cells = []
        self.Shifts = []
        
        # add this Image to the parent Job, if the Job is defined. `Images` image library objects don't have a `parent` set.
        if self.parent:
            self.parent.add_Images( self )
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Image object:\n"
        s += " Image ID = '" + str(self.ImageID) + "'\n"
        s += " Reticle ID = '" + str(self.ReticleID) + "'\n"
        s += " --- Image Distribution ---\n" 
        if len( self.get_distribution() ) > 0:
            s += "    [CellCol,CellRow] , [ShiftX,ShiftY]\n"
        else:
            s += "    Image Not Distributed\n"
        
        ellipsis = False
        for i,ii in enumerate( self.get_distribution() ):
            if len( self.get_distribution() ) < 20 or i<10 or i>(  len( self.get_distribution() ) - 10  ):
                s += "    %000i: ["%(i) + str(ii[0]) + " , " + str(ii[1]) + "]\n"
            else:
                if ellipsis==False: 
                    s+="    ...\n"
                    ellipsis=True
                #end if(ellipse)
            #end if(10>i>len-10)
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
    
    def get_ReticleSize(self):
        '''Return the Image Size scaled to Reticle-scale (using `Job.get_LensReduction()`` ), in millimeters, [x,y].'''
        mag = self.parent.get_LensReduction()
        return (self.sizeXY[0] * mag , self.sizeXY[1] * mag)
    #end
    
    def get_ReticleShift(self):
        '''Return the Image Shift scaled to Reticle-scale (using `Job.get_LensReduction()`` ), in millimeters, [x,y].'''
        mag = self.parent.get_LensReduction()
        return (self.shiftXY[0] * mag , self.shiftXY[1] * mag)
    #end
    
    
    
    def get_ImageID(self):
        '''Return ImageID, if it has been set.  Otherwise, return `None`.'''
        return self.ImageID
    
    def set_ImageID(self, ImageID):
        '''Set ImageID, as string.'''
        self.ImageID = str(ImageID)
    
    
    
    def get_BaseImageID(self):
        '''Return BaseImageID, if it has been set (usually only for Images defined during Alignment.Mark definitions).  Otherwise, return `None`.'''
        return self.BaseImageID
    
    def set_BaseImageID(self, BaseImageID):
        '''Set BaseImageID - usually only for Images defined during Alignment.Mark definitions.'''
        self.BaseImageID = str(BaseImageID)
    
    def unset_BaseImageID(self):
        '''Unset the BaseImageID - reverts back to it's default value of `None`.'''
        self.BaseImageID = None
    
    
    
    
    ##############################################
    #       Other methods
    ##############################################
    
    def distribute(self, cellCR=None, shiftXY=[0,0]):
        """
        Distribute this Image to specified cells with specified Image-to-Cell-Shift.
        
        distribute( [Col,Row], shiftXY=[x,y] )
        
        Parameters
        ---------
        CellCR : 2-valued array-like of integers
            Cell coordinates to distribute this Image to. An Image can only be distributed into a Cell once.  To distribute the same reticle image onto a Cell multiple times, define separate Images for each insertion. Eg. [1,3] or [-5,10]
        ShiftXY : 2-valued array-like of coordinates, optional
            X/Y coordinates for shifting the image insertion, with respect to the center of the Cell (aka. "Image-to-Cell Shift"). Defaults to [0,0]
            (future) logic if Cell is outside wafer diam?  
            warns if shift >= cell size / 2
        """
        if len(cellCR) != 2:
            raise ValueError( "Expected x,y pair of numbers for cellCR, instead got: " + str(cellCR) )
        elif ( cellCR[0] != int(cellCR[0]) ) or ( cellCR[1] != int(cellCR[1]) ):
            raise ValueError( "Expected x,y to be integers, instead got: " + str(cellCR) )
        else:
            self.Cells.append(   ( cellCR[0], cellCR[1] )   )
        #end if(cellCR)
        
        if len(shiftXY) != 2:
            raise ValueError( "Expected x,y pair of numbers for cellCR, instead got: " + str(cellCR) )
        else:
            self.Shifts.append(   ( shiftXY[0], shiftXY[1] )   )
    #end Distribute()
    
    def get_distribution(self):
        '''Return list of [CellC,CellR], [ShiftX,ShiftY] pairs corresponding to each distribution of this Image.'''
        return list( zip(self.Cells, self.Shifts) )
    
  
#end class(Image)


################################################
################################################


