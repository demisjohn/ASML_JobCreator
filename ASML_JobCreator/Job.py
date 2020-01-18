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
        self.defaults = Defaults
        
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
            if WARN(): print("Using default values for Job `comment`.")
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
        return Layer( LayerID=LayerID, CombinedWithZeroLayer=CombinedWithZeroLayer, parent=self)
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
    
    def export(self, filepath="ASML_Job.txt"):
        """
        Export an ASCII text file of this job, that can be imported by the ASML PAS software (with Job Creator software option installed).
    
        Parameters
        ----------
        filepath : string
            Path to save the text file to.  
        """
        s = self.__genascii()       # get the text to write
        ascii = s.encode('ascii')
        
        # open the file & write it:
        with open(filepath, 'wb') as f:
            if DEBUG(): print( "Opened file for writing at %s" %filepath)
            f.write(ascii)
        #end with file(filepath)
        if DEBUG(): print("Job.export(): ASCII Text file written succesfully.")
    #end export()
    
    
    def __genascii(self):
        """
        Return ASCII string for writing to a file, in ASML PAS compatible format. Pulls in all object data as defined by user.
        """
        if DEBUG(): print("Job.__genascii(): Generating ASCII Text...")
        tab = '   '
        col1 = 50       # Num Characters to offset column 1
        
        def indent(startstr='', spc = ' ', indent=col1):
            """Return a string containing enough spaces so that any following text is indented `col1` characters, after `startstr`."""
            return spc * (  indent - len(startstr)  )
        #end indent()
        
        def add(string="", cmd='', val=[0,0], tab=tab, integers=False):
            """Returns input `string` + `cmd` + `val` with the appropriate tab, indent and newlines.
            
            Parameters
            ----------
            string : str
                The string that the result should be appended to.
            cmd : str
                The command or variable name to insert into the string, first text on the line.
            val : { str | 2-valued array-like of numbers }
                Value of the above command/variable, second text on the line.
            tab : str, optional
                Text to use as a tab, defaults to 3 spaces '   '.
            integers : { True | False }, optional
                If True, 2-valued iterables will be inserted as quoted integers, eg.
                    "10" "-5"
                which is the case for cell selection/indexing.  If False, use floats with precision of 6, eg:
                    10.000000 -5.000000
                Which is the case for arbitrary X/Y coordinates. 
                Defaults to False.
            """
            s1 = tab + cmd
            if isinstance(val, str):
                s2 = indent(s1) + '"' + val + '"'
            elif np.size(val) == 2:
                if not integers:
                    s2 = indent(s1) + "%0.6f %0.6f" % tuple(val) # X/Y coords
                else:
                    s2 = indent(s1) + '"%i" "%i"' % tuple(val)  # Cell Index, quoted
                #end if(cells)
            elif np.size(val) == 3:
                if not integers:
                    s2 = indent(s1) + "%0.6f %0.6f %0.6f" % tuple(val) # unused
                else:
                    s2 = indent(s1) + '%i %i %i' % tuple(val)  # RTCL_CHECK_LIMITS_UPPER, unquoted
                #end if(cells)
            elif np.size(val) == 4:
                if not integers:
                    s2 = indent(s1) + "%0.6f %0.6f %0.6f %0.6f" % tuple(val) # CORR_80_88_MARK_SHIFT
                else:
                    s2 = indent(s1) + '%i %i %i %i' % tuple(val)  # unused
                #end if(cells)
            else:
                if not integers:
                    s2 = indent(s1) + "%0.6f" % (val)
                else:
                    s2 = indent(s1) + '%i' % (val)  # layer ID #
                #end if(integers)
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
        
        
        if DEBUG(): print("Generating Text Sections 'IMAGE_DEFINITION' & 'IMAGE_DISTRIBUTION'")
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
                s = add(s, "CELL_SELECTION", D[0], integers=True)
                s = add(s, "DISTRIBUTION_ACTION", Defaults.Image_DISTRIBUTION_ACTION)
                s = add(s, "OPTIMIZE_ROUTE", Defaults.Image_OPTIMIZE_ROUTE)
                s = add(s, "IMAGE_CELL_SHIFT", D[1])
                s += "END_SECTION\n"
                s += "\n"
            #end for(dist)
            s += "\n\n\n"
        #end for(ImageList)
        
        s += "\n\n"
        
        
        
        if DEBUG(): print("Generating Text Section 'LAYER_DEFINITION'")
        for i,L in enumerate(self.LayerList):
            if DEBUG(): print( "Layer #%i, ID='%s'" %(i, str(L.LayerID) ) )
            s += "START_SECTION LAYER_DEFINITION\n"
            s = add(s, "LAYER_NO", i, integers=True)
            if L.LayerID.isalnum():
                LyrIDstr = L.LayerID
            else:
                warnstr = 'Layer # %i: Layer ID string "%s" is invalid, setting ID string to layer number.' % (i, str(L.LayerID))
                if WARN(): print(warnstr)
                LyrIDstr = str(i)
                L.LayerID = LyrIDstr
            #end if(LayerID is alphanumeric)
            s = add(s, "LAYER_ID", LyrIDstr)
            s = add(s, "WAFER_SIDE", Defaults.Layer_WAFER_SIDE)
            s += "END_SECTION\n"
            s += "\n"
        #end for(LayerList)
        
        s += "\n\n"
        
        
        ################
        # Process Data #
        ################
        if DEBUG(): print("Generating Text Section 'PROCESS_DATA'...")
        for i,L in enumerate(self.LayerList):
            s += "START_SECTION PROCESS_DATA\n"
            s = add(s, "LAYER_ID", L.LayerID)
            s = add(s, "LENS_REDUCTION", Defaults.ProcessData_LENS_REDUCTION, integers=True)
            s = add(s, "CALIBRATION", Defaults.ProcessData_CALIBRATION)
            
            s = add(s, "OPTICAL_PREALIGNMENT", Defaults.ProcessData_OPTICAL_PREALIGNMENT)
            """
            if alignment:
                OPTICAL_PREALIGNMENT                          "Y"  (see above)
               OPT_PREALIGN_MARKS                            "S" "N"
               GLBL_WFR_ALIGNMENT                            "N"
            """
            
            s = add(s, "COO_REDUCTION", Defaults.ProcessData_COO_REDUCTION)
            s = add(s, "MIN_NUMBER_PULSES_IN_SLIT", Defaults.ProcessData_MIN_NUMBER_PULSES_IN_SLIT)
            s = add(s, "MIN_NUMBER_PULSES", Defaults.ProcessData_MIN_NUMBER_PULSES, integers=True)
            s = add(s, "SKIP_COARSE_WAFER_ALIGN", Defaults.ProcessData_SKIP_COARSE_WAFER_ALIGN)
            s = add(s, "REDUCE_RETICLE_ALIGN", Defaults.ProcessData_REDUCE_RETICLE_ALIGN)
            s = add(s, "REDUCE_RA_DRIFT", Defaults.ProcessData_REDUCE_RA_DRIFT)
            s = add(s, "REDUCE_RA_INTERVAL", Defaults.ProcessData_REDUCE_RA_INTERVAL, integers=True)
            s = add(s, "RET_COOL_CORR", Defaults.ProcessData_RET_COOL_CORR)
            s = add(s, "RET_COOL_TIME", Defaults.ProcessData_RET_COOL_TIME, integers=True)
            s = add(s, "RET_COOL_START_ON_LOAD", Defaults.ProcessData_RET_COOL_START_ON_LOAD)
            s = add(s, "RET_COOL_USAGE", Defaults.ProcessData_RET_COOL_USAGE)
            s = add(s, "GLBL_OVERLAY_ENHANCEMENT", Defaults.ProcessData_GLBL_OVERLAY_ENHANCEMENT)
            
            ### layer shift:
            s = add(s, "LAYER_SHIFT", L.get_LayerShift() )
            
            """
            IF alignment:
                CORR_WAFER_GRID                               "Default"
                NR_OF_MARKS_TO_USE                            2
                MIN_MARK_DISTANCE_COARSE                      20.000000
                MIN_MARK_DISTANCE                             40
                MAX_80_88_SHIFT                               0.500000
                MAX_MARK_RESIDUE                              200.000000
                SPM_MARK_SCAN                                 "S"
                ERR_DETECTION_88_8                            "M"
            """
            
            
            s = add(s, "CORR_INTER_FLD_EXPANSION", Defaults.ProcessData_CORR_INTER_FLD_EXPANSION)
            s = add(s, "CORR_INTER_FLD_NONORTHO", Defaults.ProcessData_CORR_INTER_FLD_NONORTHO)
            s = add(s, "CORR_INTER_FLD_ROTATION", Defaults.ProcessData_CORR_INTER_FLD_ROTATION)
            s = add(s, "CORR_INTER_FLD_TRANSLATION", Defaults.ProcessData_CORR_INTER_FLD_TRANSLATION)
            s = add(s, "CORR_INTRA_FLD_MAGNIFICATION", Defaults.ProcessData_CORR_INTRA_FLD_MAGNIFICATION)
            s = add(s, "CORR_INTRA_FLD_ROTATION", Defaults.ProcessData_CORR_INTRA_FLD_ROTATION)
            s = add(s, "CORR_INTRA_FLD_TRANSLATION", Defaults.ProcessData_CORR_INTRA_FLD_TRANSLATION)
            s = add(s, "CORR_INTRA_FLD_ASYM_ROTATION", Defaults.ProcessData_CORR_INTRA_FLD_ASYM_ROTATION)
            s = add(s, "CORR_INTRA_FLD_ASYM_MAGN", Defaults.ProcessData_CORR_INTRA_FLD_ASYM_MAGN)
            s = add(s, "CORR_PREALIGN_ROTATION", Defaults.ProcessData_CORR_PREALIGN_ROTATION)
            s = add(s, "CORR_PREALIGN_TRANSLATION", Defaults.ProcessData_CORR_PREALIGN_TRANSLATION)
            
            ## 4 floats:
            s = add(s, "CORR_80_88_MARK_SHIFT", Defaults.ProcessData_CORR_80_88_MARK_SHIFT)
            s = add(s, "CORR_LENS_HEATING", Defaults.ProcessData_CORR_LENS_HEATING)
            
            """
                NUMERICAL_APERTURE                            0.570000
                SIGMA_OUTER                                   0.750000
            """            
            
            s = add(s, "RTCL_CHECK_SURFACES", Defaults.ProcessData_RTCL_CHECK_SURFACES)
            
            ## 3 ints
            s = add(s, "RTCL_CHECK_LIMITS_UPPER", Defaults.ProcessData_RTCL_CHECK_LIMITS_UPPER, integers=True)
            s = add(s, "RTCL_CHECK_LIMITS_LOWER", Defaults.ProcessData_RTCL_CHECK_LIMITS_LOWER, integers=True)
            
            """
            IF alignment:
                   ALIGNMENT_METHOD                              "T"
            """
            
            s = add(s, "CLOSE_GREEN_LASER_SHUTTER", Defaults.ProcessData_CLOSE_GREEN_LASER_SHUTTER)
            s = add(s, "REALIGNMENT_METHOD", Defaults.ProcessData_REALIGNMENT_METHOD)
            s = add(s, "IMAGE_ORDER_OPTIMISATION", Defaults.ProcessData_IMAGE_ORDER_OPTIMISATION)
            s = add(s, "RETICLE_ALIGNMENT", Defaults.ProcessData_RETICLE_ALIGNMENT)
            s = add(s, "USE_DEFAULT_RETICLE_ALIGNMENT_METHOD", Defaults.ProcessData_USE_DEFAULT_RETICLE_ALIGNMENT_METHOD)
            s = add(s, "CRITICAL_PERCENTAGE", Defaults.ProcessData_CRITICAL_PERCENTAGE, integers=True)
            s = add(s, "SHARE_LEVEL_INFO", Defaults.ProcessData_SHARE_LEVEL_INFO)
            s = add(s, "FOCUS_EDGE_CLEARANCE", Defaults.ProcessData_FOCUS_EDGE_CLEARANCE)
            
            """
            IF alignment:
                   INLINE_Q_ABOVE_P_CALIBRATION                  "M"
            else: .... """
            s = add(s, "INLINE_Q_ABOVE_P_CALIBRATION", Defaults.ProcessData_INLINE_Q_ABOVE_P_CALIBRATION)
            
            ## SMS?
            s = add(s, "SHIFTED_MEASUREMENT_SCANS", Defaults.ProcessData_SHIFTED_MEASUREMENT_SCANS)
            s = add(s, "FOCUS_MONITORING", Defaults.ProcessData_FOCUS_MONITORING)
            s = add(s, "FOCUS_MONITORING_SCANNER", Defaults.ProcessData_FOCUS_MONITORING_SCANNER)
            s = add(s, "DYN_PERF_MONITORING", Defaults.ProcessData_DYN_PERF_MONITORING)
            s = add(s, "FORCE_MEANDER_ENABLED", Defaults.ProcessData_FORCE_MEANDER_ENABLED)
            s += "END_SECTION\n\n"
        # end for(LayerList)
        
        s += "\n\n"
        
        ################
        # Reticle Data #
        ################
        if DEBUG(): print("Generating Text Section 'RETICLE_DATA'...")
        for i,L in enumerate(self.LayerList):
            if DEBUG(): print(   " RETICLE_DATA: Layer %i, '%s'" % ( i, str(L.LayerID) )   )
            for ii,I in enumerate(L.ImageList):
                if DEBUG(): print(   "  RETICLE_DATA: Image %i, '%s'" % ( ii, str(I.ImageID) )   )
                s += "START_SECTION RETICLE_DATA\n"
                s = add(s, "LAYER_ID", L.LayerID)
                s = add(s, "IMAGE_ID", I.ImageID)
                s = add(s, "IMAGE_USAGE", "Y")
                s = add(s, "RETICLE_ID", I.ReticleID)
                s = add(s, "IMAGE_SIZE", I.sizeXY )
                s = add(s, "IMAGE_SHIFT", I.shiftXY )
                s = add(s, "MASK_SIZE", I.sizeXY )
                s = add(s, "MASK_SHIFT", I.shiftXY )
                s = add(s, "ENERGY_ACTUAL", L.EnergyList[i] )
                s = add(s, "FOCUS_ACTUAL", L.FocusList[i] )
                s = add(s, "FOCUS_TILT", L.FocusTiltList[i] )
                s = add(s, "NUMERICAL_APERTURE", L.NAList[i] )
                s = add(s, "SIGMA_OUTER", L.Sig_oList[i] )
                if L.Sig_iList[i]: s = add(s, "SIGMA_INNER", L.Sig_iList[i] ) 
                s = add(s, "IMAGE_EXPOSURE_ORDER", 0, integers=True ) # IMAGE_EXPOSURE_ORDER 0
                s = add(s, "LITHOGRAPHY_PROCESS", L.IlluminationModeList[i] )
                s = add(s, "IMAGE_INTRA_FLD_COR_TRANS", Defaults.ReticleData_IMAGE_INTRA_FLD_COR_TRANS )
                s = add(s, "IMAGE_INTRA_FLD_COR_ROT", Defaults.ReticleData_IMAGE_INTRA_FLD_COR_ROT )
                s = add(s, "IMAGE_INTRA_FLD_COR_MAG", Defaults.ReticleData_IMAGE_INTRA_FLD_COR_MAG )
                s = add(s, "IMAGE_INTRA_FLD_COR_ASYM_ROT", Defaults.ReticleData_IMAGE_INTRA_FLD_COR_ASYM_ROT )
                s = add(s, "IMAGE_INTRA_FLD_COR_ASYM_MAG", Defaults.ReticleData_IMAGE_INTRA_FLD_COR_ASYM_MAG )
                s = add(s, "LEVEL_METHOD_Z", Defaults.ReticleData_LEVEL_METHOD_Z )
                s = add(s, "LEVEL_METHOD_RX", Defaults.ReticleData_LEVEL_METHOD_RX )
                s = add(s, "LEVEL_METHOD_RY", Defaults.ReticleData_LEVEL_METHOD_RY )
                s = add(s, "DIE_SIZE_DEPENDENCY", Defaults.ReticleData_DIE_SIZE_DEPENDENCY )
                s = add(s, "ENABLE_EFESE", Defaults.ReticleData_ENABLE_EFESE )
                s = add(s, "CD_FEC_MODE", Defaults.ReticleData_CD_FEC_MODE )
                s = add(s, "DOSE_CORRECTION", Defaults.ReticleData_DOSE_CORRECTION )
                s = add(s, "DOSE_CRITICAL_IMAGE", Defaults.ReticleData_DOSE_CRITICAL_IMAGE )
                s = add(s, "GLOBAL_LEVEL_POINT_1", Defaults.ReticleData_GLOBAL_LEVEL_POINT_1 )
                s = add(s, "GLOBAL_LEVEL_POINT_2", Defaults.ReticleData_GLOBAL_LEVEL_POINT_2 )
                s = add(s, "GLOBAL_LEVEL_POINT_3", Defaults.ReticleData_GLOBAL_LEVEL_POINT_3 )
            
                s += "END_SECTION\n\n"
            #end for(ImageList)
        # end for(LayerList)
        
        
        if DEBUG(): print("Job.__genascii(): done generating ASCII string.")
        return s
    #end __genascii()
#end class(Job)



################################################
################################################


