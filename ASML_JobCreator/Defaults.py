"""
This file is part of the ASML_JobCreator package for Python 3.x.

defaults.py
    Contains & instantiates object of class Default, 
    containing hard-coded defualt values for many options.
    
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
        s += str( self.__dict__ )
        
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
        
        ########################################
        #
        #   Defaults for user-settings
        #
        ########################################
        self.comment_line1 = "Created with python ASML_JobCreator"
        self.comment_line2 = "Univ. of California Santa Barbara"
        self.comment_line3 = "UCSB Nanofab, Demis D. John"
        
        
        ## Defaults Hard-Coded here:
        self.MACHINE_TYPE = "PAS5500/300"
        self.RETICLE_SIZE = 6        # inches
        self.WFR_DIAMETER = 100.0       # mm
        self.WFR_FLAT_LENGTH = 32.5     # mm, used for MPL plotting only, custom param
        self.WFR_NOTCH = "N"
        self.COVER_MODE = "W"
        self.PLACEMENT_MODE = "O"
        self.PREALIGN_METHOD = "STANDARD"
        self.WAFER_ROTATION = 0.0
        self.MATCHING_SET_ID = "DEFAULT"
    
        ## Cell Structure:
        self.ROUND_EDGE_CLEARANCE = 5.0
        self.FLAT_EDGE_CLEARANCE = 5.0
        self.EDGE_EXCLUSION = 3.0
        self.NUMBER_DIES = [1, 1]       # number of Die per Cell
        self.MIN_NUMBER_DIES = 1
    
    
    
        ## Params editable by user:
        self.CELL_SIZE = [10, 10]    #mm
        self.MATRIX_SHIFT = [0.0, 0.0]
        self.COMBINE_ZERO_FIRST = "N"
        
        
        
        ## Image Defaults
        self.Image_VARIANT_ID = ""
        self.Image_OPTIMIZE_ROUTE = "N"
        self.Image_DISTRIBUTION_ACTION = "I"
        
        
        
        ## Layer Defaults
        self.Layer_WAFER_SIDE = "A"
        
        
        
        ## Process Data > Layer Defualts
        self.ProcessData_LENS_REDUCTION                                = 4.0
        self.ProcessData_CALIBRATION                                   = "N"
        self.ProcessData_OPTICAL_PREALIGNMENT                          = "N"     # Alignment
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
        self.ProcessData_GLBL_OVERLAY_ENHANCEMENT                      = "N"
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
        
        
        
        ## Reticle Data defaults
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



