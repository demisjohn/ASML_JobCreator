"""
This file is part of the ASML_JobCreator package for Python 3.x.

defaults.py
    Contains & instantiates object of class Default, 
    containing hard-coded default values for many options.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Defaults(object):
    '''
    Class for holding all default values, whether or not they are hard-coded or user-editable.
    '''
    
    def __init__(self):
        '''inits an object with defaults set from below'''
        self.LoadDefaultValues()
    #end __init__
    
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Default object:\n"
        s += str( self.__dict__ )   # lists all the properties/values
        
        return s
    #end __str__
    
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    
    
    ###########################################
    #
    #    Default Values
    #
    ###########################################
    
    def LoadDefaultValues(self):
        
        ## Defaults for plotting options:
        self.Plotting_Alpha = 0.7       # alpha transparency value
        self.Plotting_LineWidth = 1.0
        self.Plotting_WaferColor = 'snow'
        self.Plotting_WaferEdgeColor = 'lightgrey'
        self.Plotting_BGHatch = '.........'
        self.Plotting_GridColor = 'lightgrey'
        self.Plotting_GridStyle = ":"
        
        self.Plotting_ImageColorMap = "tab20"
        self.Plotting_MarkColorMap = "Dark2"
        self.Plotting_MarkFace = "black"
        self.Plotting_MarkLineWidth = 2.0
        self.Plotting_MarkAlpha = 1.0
        
        self.Plotting_ReticleTableColor = self.Plotting_WaferEdgeColor
        self.Plotting_LensColor = "None"
        self.Plotting_ReticleBGOutlineColor = 'darkgrey'   # unused
        self.Plotting_ReticleBGOutlineStyle = ":"
        self.Plotting_ReticleBGOutlineWidth = 1.5
        self.Plotting_ReticleLensAlpha = 0.6
        self.Plotting_ReticleTableAlpha = 0.3
        
        
        
        
        ## Cell Structure:
        self.ROUND_EDGE_CLEARANCE = 2.0
        self.FLAT_EDGE_CLEARANCE = 2.0
        self.EDGE_EXCLUSION = 2.0
        self.NUMBER_DIES = [1, 1]       # number of Die per Cell
        self.MIN_NUMBER_DIES = 1
        self.CELL_SIZE = [10, 10]    #mm
        self.MATRIX_SHIFT = [0.0, 0.0]
        
        
        
        ## Machine Defaults Hard-Coded here:
        self.MACHINE_TYPE = "PAS5500/300"
        self.RETICLE_SIZE = 6           # inches
        self.WFR_DIAMETER = 100.0       # mm
        self.WFR_NOTCH = "N"
        self.COVER_MODE = "W"
        self.PLACEMENT_MODE = "O"
        self.PREALIGN_METHOD = "STANDARD"
        self.WAFER_ROTATION = 0.0
        self.MATCHING_SET_ID = "DEFAULT"
        self.ProcessData_LENS_REDUCTION = 4.0    # Magnification; DUV: 4.0 // I-Line: 5.0
        # For plotting only:
        self.RETICLE_TABLE_WINDOW = [22, 27]    # mm
        self.LENS_DIAMETER = 31.00              # mm
        self.WFR_FLAT_LENGTH = 32.5             # mm
        
        self.comment_line1 = "Created with python ASML_JobCreator"
        self.comment_line2 = "Univ. of California Santa Barbara"
        self.comment_line3 = "UCSB Nanofab, Demis D. John"
        
        
        
        ## Software Limits (PAS5500/300):
        self.ImageDistribution_MaxDistPerImage = 999
        self.Image_MinImageSize = [0.0001,0.0001]   # mm <-- not checked currently
        self.Image_MaxImageSize = [26.0,33.0]   # mm <-- not checked currently
        self.Cell_MinCellSize = 1.020 # mm
        # self.Cell_MaxCellSize = 100.0 # mm <-- not checked currently
        
        
        
        ## Image Defaults
        self.Image_VARIANT_ID = ""
        self.Image_OPTIMIZE_ROUTE = "N"
        self.Image_DISTRIBUTION_ACTION = "I"
        
        
        ## Alignment Marks
        self.AlignmentMark_MARK_EDGE_CLEARANCE = "L"
        self.AlignmentMark_WAFER_SIDE = "A"
        
        
        ## Alignment Strategy
        self.AlignmentStrategy_WAFER_ALIGNMENT_METHOD = "T"
        self.AlignmentStrategy_MIN_MARK_DISTANCE_COARSE = 20.000000
        self.AlignmentStrategy_MIN_MARK_DISTANCE = 40
        self.AlignmentStrategy_MAX_80_88_MARK_SHIFT = 0.500000
        self.AlignmentStrategy_MAX_MARK_RESIDUE = 200.000000
        self.AlignmentStrategy_SPM_MARK_SCAN = "S"
        self.AlignmentStrategy_CORR_WAFER_GRID = "Default"
        self.AlignmentStrategy_ERR_DETECTION_88_8 = "M"
        self.AlignmentStrategy_GRID_OPTIMISATION_ALGORITHM = "N"
        self.AlignmentStrategy_FLYER_REMOVAL_THRESHOLD = 0.000000
        self.AlignmentStrategy_ALIGNMENT_MONITORING = "D"
        self.AlignmentStrategy_GLBL_MARK_USAGE = "A"
        
        
        ## Layer Defaults
        self.Layer_WAFER_SIDE = "A"
        
        
        ## Process Data > Layer Defaults
        self.COMBINE_ZERO_FIRST                                        = "N"
        self.ProcessData_CALIBRATION                                   = "N"
        self.ProcessData_OPTICAL_PREALIGNMENT                          = "N"
        self.ProcessData_COO_REDUCTION                                 = "D"
        self.ProcessData_MIN_NUMBER_PULSES_IN_SLIT                     = "D"
        self.ProcessData_MIN_NUMBER_PULSES                             = 21
        self.ProcessData_SKIP_COARSE_WAFER_ALIGN                       = "N"
        self.ProcessData_REDUCE_RETICLE_ALIGN                          = "N"
        self.ProcessData_REDUCE_RA_DRIFT                               = 5.000000
        self.ProcessData_REDUCE_RA_INTERVAL                            = 2
        self.ProcessData_RET_COOL_CORR                                 = "D"
        self.ProcessData_RET_COOL_TIME                                 = 0
        self.ProcessData_RET_COOL_START_ON_LOAD                        = "Y"
        self.ProcessData_RET_COOL_USAGE                                = "W"
        self.ProcessData_GLBL_RTCL_ALIGNMENT                           = "N"
        self.ProcessData_GLBL_OVERLAY_ENHANCEMENT                      = "N"
        self.ProcessData_GLBL_SYM_ALIGNMENT                            = "N"
        self.ProcessData_LAYER_SHIFT                                   = [0.000000, 0.000000]
        self.ProcessData_CORR_INTER_FLD_EXPANSION                      = [0.000000, 0.000000]
        self.ProcessData_CORR_INTER_FLD_NONORTHO                       = 0.000000
        self.ProcessData_CORR_INTER_FLD_ROTATION                       = 0.000000
        self.ProcessData_CORR_INTER_FLD_TRANSLATION                    = [0.000000, 0.000000]
        self.ProcessData_CORR_INTRA_FLD_MAGNIFICATION                  = 0.000000
        self.ProcessData_CORR_INTRA_FLD_ROTATION                       = 0.000000
        self.ProcessData_CORR_INTRA_FLD_TRANSLATION                    = [0.000000, 0.000000]
        self.ProcessData_CORR_INTRA_FLD_ASYM_ROTATION                  = 0.000000
        self.ProcessData_CORR_INTRA_FLD_ASYM_MAGN                      = 0.000000
        self.ProcessData_CORR_PREALIGN_ROTATION                        = 0.000000
        self.ProcessData_CORR_PREALIGN_TRANSLATION                     = [0.000000, 0.000000]
        self.ProcessData_CORR_80_88_MARK_SHIFT                         = [0.000000, 0.000000, 0.000000, 0.000000]
        self.ProcessData_CORR_LENS_HEATING                             = 1.000000
        self.ProcessData_RTCL_CHECK_SURFACES                           = "N"
        self.ProcessData_RTCL_CHECK_LIMITS_UPPER                       = [50000, 50000, 50000]
        self.ProcessData_RTCL_CHECK_LIMITS_LOWER                       = [50000, 50000, 50000]
        self.ProcessData_CLOSE_GREEN_LASER_SHUTTER                     = "N"
        self.ProcessData_REALIGNMENT_METHOD                            = "D"
        self.ProcessData_IMAGE_ORDER_OPTIMISATION                      = "Y"
        self.ProcessData_RETICLE_ALIGNMENT                             = "T"
        self.ProcessData_USE_DEFAULT_RETICLE_ALIGNMENT_METHOD          = "N"
        self.ProcessData_CRITICAL_PERCENTAGE                           = 83
        self.ProcessData_SHARE_LEVEL_INFO                              = "N"
        self.ProcessData_FOCUS_EDGE_CLEARANCE                          = 3.000000
        self.ProcessData_INLINE_Q_ABOVE_P_CALIBRATION                  = "D"
        self.ProcessData_SHIFTED_MEASUREMENT_SCANS                     = "N"
        self.ProcessData_FOCUS_MONITORING                              = "D"
        self.ProcessData_FOCUS_MONITORING_SCANNER                      = "D"
        self.ProcessData_DYN_PERF_MONITORING                           = "D"
        self.ProcessData_FORCE_MEANDER_ENABLED                         = "N"
        
        self.ProcessData_CORR_WAFER_GRID                               = self.AlignmentStrategy_CORR_WAFER_GRID
        self.ProcessData_MIN_MARK_DISTANCE_COARSE                      = self.AlignmentStrategy_MIN_MARK_DISTANCE_COARSE
        self.ProcessData_MIN_MARK_DISTANCE                             = self.AlignmentStrategy_MIN_MARK_DISTANCE
        self.ProcessData_MAX_80_88_SHIFT                               = self.AlignmentStrategy_MAX_80_88_MARK_SHIFT
        self.ProcessData_MAX_MARK_RESIDUE                              = self.AlignmentStrategy_MAX_MARK_RESIDUE
        self.ProcessData_SPM_MARK_SCAN                                 = self.AlignmentStrategy_SPM_MARK_SCAN
        self.ProcessData_ERR_DETECTION_88_8                            = self.AlignmentStrategy_ERR_DETECTION_88_8
        self.ProcessData_ALIGNMENT_METHOD                              = self.AlignmentStrategy_WAFER_ALIGNMENT_METHOD
        
        
        
        ## Reticle Data defaults
        #   Disabled, required to be set by user:
        #self.ReticleData_IMAGE_USAGE                                   = "Y"
        #self.ReticleData_RETICLE_ID                                    = "UCSB-OPC1"
        #self.ReticleData_IMAGE_SIZE                                    = 2.420000 4.020000
        #self.ReticleData_IMAGE_SHIFT                                   = 2.740000 5.400000
        #self.ReticleData_MASK_SIZE                                     = 2.424000 4.024000
        #self.ReticleData_MASK_SHIFT                                    = 2.744000 5.400000
        self.ReticleData_ENERGY_ACTUAL                                 = 20.000000
        self.ReticleData_FOCUS_ACTUAL                                  = 0.000000
        self.ReticleData_FOCUS_TILT                                    = [0.000000, 0.000000]
        self.ReticleData_NUMERICAL_APERTURE                            = 0.570000
        self.ReticleData_SIGMA_OUTER                                   = 0.750000
        self.ReticleData_IMAGE_EXPOSURE_ORDER                          = 0
        self.ReticleData_LITHOGRAPHY_PROCESS                           = "Default"
        self.ReticleData_IMAGE_INTRA_FLD_COR_TRANS                     = [0.000000, 0.000000]
        self.ReticleData_IMAGE_INTRA_FLD_COR_ROT                       = 0.000000
        self.ReticleData_IMAGE_INTRA_FLD_COR_MAG                       = 0.000000
        self.ReticleData_IMAGE_INTRA_FLD_COR_ASYM_ROT                  = 0.000000
        self.ReticleData_IMAGE_INTRA_FLD_COR_ASYM_MAG                  = 0.000000
        self.ReticleData_LEVEL_METHOD_Z                                = "D"
        self.ReticleData_LEVEL_METHOD_RX                               = "D"
        self.ReticleData_LEVEL_METHOD_RY                               = "D"
        self.ReticleData_DIE_SIZE_DEPENDENCY                           = "N"
        self.ReticleData_ENABLE_EFESE                                  = "N"
        self.ReticleData_CD_FEC_MODE                                   = "N"
        self.ReticleData_DOSE_CORRECTION                               = "N"
        self.ReticleData_DOSE_CRITICAL_IMAGE                           = "Y"
        self.ReticleData_GLOBAL_LEVEL_POINT_1                          = [0.000000, 0.000000]
        self.ReticleData_GLOBAL_LEVEL_POINT_2                          = [0.000000, 0.000000]
        self.ReticleData_GLOBAL_LEVEL_POINT_3                          = [0.000000, 0.000000]
        
    #end LoadDefaultValues()
    
#end class(Default)



################################################
################################################



