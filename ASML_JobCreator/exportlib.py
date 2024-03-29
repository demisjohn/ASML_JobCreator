"""
This file is part of the ASML_JobCreator package for Python 3.x.

exportlib.py
    Contains the functions necessary for generating the ASCII text file.
    
- - - - - - - - - - - - - - -

2022-08-13: Added "WAFER_ALIGHN_REPEATS" sections into PROCESS_DATA sections - needed for compatibility with LIPC system.

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.

####################################################

def _genascii(JobObj):
    """
    Return ASCII string for writing to a file, in ASML PAS compatible format. Pulls in all Job object data as defined by `JobObj``.
    """
    if DEBUG(): print("Job.__genascii(): Generating ASCII Text...")
    
    tab = '   '
    col1 = 50       # Num Characters to offset column 1
    
    
    def indent(startstr='', spc = ' ', indent=col1):
        """Return a string containing enough spaces so that any following text is indented `col1` characters, after `startstr`."""
        return spc * (  indent - len(startstr)  )
    #end indent()
    
    
    def add(string="", cmd='', val=[0,0], tab=tab, integers=False, doublestr=False, quoted=True):
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
        
        doublestr : { True | False }, optional
            If True, inserts a two-valued iterable as two quoted strings.
            For ` OPT_PREALIGN_MARKS = "Mark1" "Mark2" `
            
        quoted : { True | False }, optional
            Optionally force the removal of quotes for 2-valued integers by setting this to `False`, such as for NUMBER_DIES. Defaults to True.
        """
        s1 = tab + cmd
        if isinstance(val, str):
            if quoted:
                s2 = indent(s1) + '"' + val + '"'  # add quotes
            else:
                s2 = indent(s1) + val  # remove quotes
            #end if(quoted)
        elif np.size(val) == 1:
            if not integers:
                s2 = indent(s1) + "%0.6f" % (val)
            else:
                s2 = indent(s1) + '%i' % (val)  # layer ID #
            #end if(integers)
        elif np.size(val) == 2:
            if doublestr:
                s2 = indent(s1) + '"%s" "%s"' % tuple(val) # two strings, Opt.Prealign Marks
            elif integers:
                if quoted:
                    s2 = indent(s1) + '"%i" "%i"' % tuple(val)  # Cell Index, quoted
                else:
                    s2 = indent(s1) + '%i %i' % tuple(val)  # NUMBER_DIES, unquoted
                #end if(quoted)            
            else:
                s2 = indent(s1) + "%0.6f %0.6f" % tuple(val) # X/Y coords
            #end if(doublstr/integers)
        elif np.size(val) == 3:
            if not integers:
                s2 = indent(s1) + "%0.6f %0.6f %0.6f" % tuple(val) # unused
            else:
                s2 = indent(s1) + '%i %i %i' % tuple(val)  # RTCL_CHECK_LIMITS_UPPER, unquoted
            #end if(integers)
        elif np.size(val) == 4:
            if not integers:
                s2 = indent(s1) + "%0.6f %0.6f %0.6f %0.6f" % tuple(val) # CORR_80_88_MARK_SHIFT
            else:
                s2 = indent(s1) + '%i %i %i %i' % tuple(val)  # unused
            #end if(integers)
        elif np.size(val) == 10:
            if DEBUG(): print("DEBUG: export_lib(): np.size(val) == 10")
            if not integers:
                s2 = indent(s1) + "%0.6f %0.6f %0.6f %0.6f %0.6f %0.6f %0.6f %0.6f %0.6f %0.6f" % tuple(val) # unused
            else:
                s2 = indent(s1) + '%i %i %i %i %i %i %i %i %i %i' % tuple(val)  # for ALIGN_REPEAT_INTERVAL
            #end if(integers)
        else:
            raise ValueError("Unrecognized value type - unsure how to format for export string.")
        #end if(str/np.size)
        return string + s1 + s2 + "\n"
    #end add()
    
    
    align = bool(JobObj.Alignment)  # whether alignment sections are enabled
    if DEBUG(): print(  "Alignment sections are " + ("enabled." if align else "disabled.")  )
    
    
    s = ''
    s += "\n\n"
    s += "START_SECTION GENERAL\n"
    s = add(s, "COMMENT", JobObj.get_comment()[0] )
    s = add(s, "", JobObj.get_comment()[1] )
    s = add(s, "", JobObj.get_comment()[2] )
    s = add(s, "MACHINE_TYPE", Defaults.MACHINE_TYPE)
    s = add(s, "RETICLE_SIZE", Defaults.RETICLE_SIZE, integers=True)
    s = add(s, "WFR_DIAMETER", Defaults.WFR_DIAMETER)
    s = add(s, "WFR_NOTCH", Defaults.WFR_NOTCH)
    s = add(s, "CELL_SIZE", JobObj.Cell.get_CellSize() )
    s = add(s, "ROUND_EDGE_CLEARANCE", JobObj.Cell.get_RoundEdgeClearance() )
    s = add(s, "FLAT_EDGE_CLEARANCE", JobObj.Cell.get_FlatEdgeClearance() )
    s = add(s, "EDGE_EXCLUSION", JobObj.Cell.get_EdgeExclusion() )
    s = add(s, "COVER_MODE", Defaults.COVER_MODE)
    s = add(s, "NUMBER_DIES", JobObj.Cell.get_NumberDiePerCell() , integers=True, quoted=False)
    s = add(s, "MIN_NUMBER_DIES", JobObj.Cell.get_MinNumberDie() , integers=True)
    s = add(s, "PLACEMENT_MODE", Defaults.PLACEMENT_MODE)
    s = add(s, "MATRIX_SHIFT", JobObj.Cell.get_MatrixShift())
    s = add(s, "PREALIGN_METHOD", Defaults.PREALIGN_METHOD)
    if JobObj.get_CombinedZeroFirst():
        s = add(s, "COMBINE_ZERO_FIRST", "Y")
    else:
        s = add(s, "COMBINE_ZERO_FIRST", Defaults.COMBINE_ZERO_FIRST)
    s = add(s, "WAFER_ROTATION", Defaults.WAFER_ROTATION)
    s = add(s, "MATCHING_SET_ID", Defaults.MATCHING_SET_ID)
    s += "END_SECTION\n"
    s += "\n\n\n\n\n"
    
    
    if align:
        if DEBUG(): print("Generating Text Sections 'ALIGNMENT_MARK'")
        for i,M in enumerate( JobObj.Alignment.MarkList ):
            if DEBUG(): print("Mark %i: `%s`" % (i,M.MarkID) )
            s += "START_SECTION ALIGNMENT_MARK\n"
            s = add(s, "MARK_ID", M.MarkID)
            s = add(s, "IMAGE_ID", M.Image.ImageID)
            s = add(s, "MARK_EDGE_CLEARANCE", Defaults.AlignmentMark_MARK_EDGE_CLEARANCE)
            s = add(s, "WAFER_SIDE", Defaults.AlignmentMark_WAFER_SIDE)
            s = add(s, "MARK_LOCATION", M.waferXY)
            s += "END_SECTION\n\n"
        #end for(markslist)
        
        s += "\n\n\n\n\n"
        
        if DEBUG(): print("Generating Text Sections 'WFR_ALIGN_STRATEGY'")
        for i,S in enumerate( JobObj.Alignment.StrategyList ):
            if DEBUG(): print("Strategy %i: `%s`" % (i,S.get_ID()) )
            s += "START_SECTION WFR_ALIGN_STRATEGY\n"
            s = add(s, "STRATEGY_ID", S.get_ID() )
            s = add(s, "WAFER_ALIGNMENT_METHOD", Defaults.AlignmentStrategy_WAFER_ALIGNMENT_METHOD)
            s = add(s, "NR_OF_MARKS_TO_USE", S.get_required_marks(), integers=True)
            s = add(s, "NR_OF_X_MARKS_TO_USE", S.get_required_marks(), integers=True)
            s = add(s, "NR_OF_Y_MARKS_TO_USE", S.get_required_marks(), integers=True)
            s = add(s, "MIN_MARK_DISTANCE_COARSE", Defaults.AlignmentStrategy_MIN_MARK_DISTANCE_COARSE)
            s = add(s, "MIN_MARK_DISTANCE", Defaults.AlignmentStrategy_MIN_MARK_DISTANCE, integers=True)
            s = add(s, "MAX_80_88_MARK_SHIFT", Defaults.AlignmentStrategy_MAX_80_88_MARK_SHIFT)
            s = add(s, "MAX_MARK_RESIDUE", Defaults.AlignmentStrategy_MAX_MARK_RESIDUE)
            s = add(s, "SPM_MARK_SCAN", Defaults.AlignmentStrategy_SPM_MARK_SCAN)
            s = add(s, "CORR_WAFER_GRID", Defaults.AlignmentStrategy_CORR_WAFER_GRID)
            s = add(s, "ERR_DETECTION_88_8", Defaults.AlignmentStrategy_ERR_DETECTION_88_8)
            s = add(s, "GRID_OPTIMISATION_ALGORITHM", Defaults.AlignmentStrategy_GRID_OPTIMISATION_ALGORITHM)
            s = add(s, "FLYER_REMOVAL_THRESHOLD", Defaults.AlignmentStrategy_FLYER_REMOVAL_THRESHOLD)
            s = add(s, "ALIGNMENT_MONITORING", Defaults.AlignmentStrategy_ALIGNMENT_MONITORING)
            s += "END_SECTION\n"
        #end for(StrategyList)
        
        s += "\n\n\n\n\n"
        
        if DEBUG(): print("Generating Text Sections 'MARK_ALIGNMENT' (Strategy<--Marks)")
        for i,S in enumerate( JobObj.Alignment.StrategyList ):
            if DEBUG(): print("Strategy %i: `%s`" % (i,S.get_ID()) )
            for ii,M in enumerate( S.MarkList ):
                if DEBUG(): print("Mark %i: `%s`" % (i,M.MarkID) )
                s += "START_SECTION MARK_ALIGNMENT\n"
                s = add(s, "STRATEGY_ID", S.get_ID() )
                s = add(s, "MARK_ID", M.MarkID )
                s = add(s, "GLBL_MARK_USAGE", Defaults.AlignmentStrategy_GLBL_MARK_USAGE)
                s = add(s, "MARK_PREFERENCE", S.MarkPrefList[ii] )
                s += "END_SECTION\n\n"
            #end for(MarkList)
            s += "\n\n"
        #end for(markslist)
        s += "\n\n\n\n\n"
    #end if(align)
    
    
    if DEBUG(): print("Generating Text Sections 'IMAGE_DEFINITION' & 'IMAGE_DISTRIBUTION'")
    for I in JobObj.ImageList:
        s += "START_SECTION IMAGE_DEFINITION\n"
        s = add(s, "IMAGE_ID", I.ImageID)
        s = add(s, "RETICLE_ID", I.ReticleID)
        s = add(s, "IMAGE_SIZE", I.get_ReticleSize() )
        s = add(s, "IMAGE_SHIFT", I.get_ReticleShift() )
        s = add(s, "MASK_SIZE", I.get_ReticleSize() )
        s = add(s, "MASK_SHIFT", I.get_ReticleShift() )
        if I.get_BaseImageID():
            s = add(s, "BASE_IMAGE_ID", I.get_BaseImageID() )   # only for Al.Marks
        s = add(s, "VARIANT_ID", Defaults.Image_VARIANT_ID)
        s += "END_SECTION\n"
        s += "\n"
    #end for(ImageList)
    
    s += "\n\n\n\n\n"
    
    for I in JobObj.ImageList:
        for D in I.get_distribution():
            s += "\n"
            s += "START_SECTION IMAGE_DISTRIBUTION\n"
            s = add(s, "IMAGE_ID", I.ImageID)
            s = add(s, "CELL_SELECTION", D[0], integers=True)
            s = add(s, "DISTRIBUTION_ACTION", Defaults.Image_DISTRIBUTION_ACTION)
            s = add(s, "OPTIMIZE_ROUTE", Defaults.Image_OPTIMIZE_ROUTE)
            s = add(s, "IMAGE_CELL_SHIFT", D[1])
            s += "END_SECTION\n"
            s += "\n\n"
        #end for(dist)
    #end for(ImageList)
    
    s += "\n\n\n\n\n"
    
    
    
    if DEBUG(): print("Generating Text Section 'LAYER_DEFINITION'")
    for i,L in enumerate(JobObj.LayerList):
        if DEBUG(): print( "Layer #%i, ID='%s'" %(i, str(L.LayerID) ) )
        s += "START_SECTION LAYER_DEFINITION\n"
        s = add(s, "LAYER_NO", i, integers=True)
        if not L.LayerID:
            warnstr = 'Layer # %i: No Layer ID string provided ("%s"), setting ID to layer number.' % (i, str(L.LayerID))
            if WARN(): print(warnstr)
            L.LayerID = str(i)
        #end if(not L.LayerID)
        LyrIDstr = L.LayerID
        #end if(LayerID is alphanumeric)
        s = add(s, "LAYER_ID", LyrIDstr)
        s = add(s, "WAFER_SIDE", Defaults.Layer_WAFER_SIDE)
        s += "END_SECTION\n"
        s += "\n"
    #end for(LayerList)
    
    s += "\n\n\n\n"
    
    
    ########################################
    # Marks + Strategy Selection per Layer #
    ########################################
    
    if DEBUG(): print("Generating Text Sections 'MARKS_SELECTION' (Layer<--Marks)")
    for i,L in enumerate(JobObj.LayerList):
        if DEBUG(): print( "Layer #%i, ID='%s'" %(i, str(L.LayerID) ) )
        s += "\n"
        for ii,M in enumerate( JobObj.Alignment.MarkList ):
            s += "START_SECTION MARKS_SELECTION\n"
            s = add(s, "LAYER_ID", L.LayerID)
            s = add(s, "MARK_ID", M.MarkID)
            if np.isin( M, L.MarkList ):
                expose="E"
            else:
                expose="N"
            s = add(s, "GLBL_MARK_USAGE", expose)
            s += "END_SECTION\n"
            s += "\n"
        #end for(MarkList)
    #end for(LayerList)
    
    s += "\n\n\n\n\n"
    
    if DEBUG(): print("Generating Text Sections 'STRATEGY_SELECTION' (Layer<--Strategy)")
    for i,L in enumerate(JobObj.LayerList):
        if L.GlobalStrategy:
            if DEBUG(): print(   "Layer #%i, ID='%s': Strategy = `%s`" %(i, str(L.LayerID) , L.GlobalStrategy.get_ID() )   )
            s += "START_SECTION STRATEGY_SELECTION\n"
            s = add(s, "LAYER_ID", L.LayerID)
            s = add(s, "STRATEGY_ID", L.GlobalStrategy.get_ID() )
            s = add(s, "STRATEGY_USAGE", "A") # "Active"
            s += "END_SECTION\n"
            s += "\n"
        #end for(MarkList)
    #end for(LayerList)
    
    s += "\n\n\n\n\n"
    
    
    ################
    # Process Data #
    ################
    if DEBUG(): print("Generating Text Section 'PROCESS_DATA'...")
    for i,L in enumerate(JobObj.LayerList):
        if DEBUG(): print(   "Layer #%i, ID='%s'" %(i, str(L.LayerID) )   )
        s += "START_SECTION PROCESS_DATA\n"
        s = add(s, "LAYER_ID", L.LayerID)
        s = add(s, "LENS_REDUCTION", JobObj.get_LensReduction(), integers=True)
        s = add(s, "CALIBRATION", Defaults.ProcessData_CALIBRATION)
        
        if align:
            if L.PreAlignMarksList:
                s = add(s, "OPTICAL_PREALIGNMENT", "Y")
                pmarks = [M.MarkID for M in L.PreAlignMarksList]
                s = add(s, "OPT_PREALIGN_MARKS", pmarks, doublestr=True)
            else:
                s = add(s, "OPTICAL_PREALIGNMENT", Defaults.ProcessData_OPTICAL_PREALIGNMENT)
        
            if L.GlobalStrategy:
                s = add(s, "GLBL_WFR_ALIGNMENT", "Y")
            else:
                s = add(s, "GLBL_WFR_ALIGNMENT", "N")
        #end if(align)
        
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
        
        if align: 
            s = add(s, "GLBL_RTCL_ALIGNMENT", Defaults.ProcessData_GLBL_RTCL_ALIGNMENT)
        s = add(s, "GLBL_OVERLAY_ENHANCEMENT", Defaults.ProcessData_GLBL_OVERLAY_ENHANCEMENT)
        if align: 
            s = add(s, "GLBL_SYM_ALIGNMENT", Defaults.ProcessData_GLBL_SYM_ALIGNMENT)
        
        # added 2022-08-13 for post-LIPC compatibility:
        s = add(s, "WAFER_ALIGN_REPEATS", Defaults.ProcessData_WAFER_ALIGN_REPEATS)
        s = add(s, "NR_WAFER_ALIGN_REPEATS", Defaults.ProcessData_NR_WAFER_ALIGN_REPEATS, integers=True)
        s = add(s, "ALIGN_REPEAT_INTERVAL", Defaults.ProcessData_ALIGN_REPEAT_INTERVAL, integers=True)
        s = add(s, "SMART_REPEAT_COUNT", Defaults.ProcessData_SMART_REPEAT_COUNT, integers=True)
        s = add(s, "SMART_REPEAT_THRESHOLD", Defaults.ProcessData_SMART_REPEAT_THRESHOLD)
        
        
        s = add(s, "LAYER_SHIFT", L.get_LayerShift() )
        
        if L.get_CombineWithZeroLayer():
            s = add(s, "NR_OF_MARKS_TO_USE", 0, integers=True)
        else:
            if L.GlobalStrategy:    
                s = add(s, "NR_OF_MARKS_TO_USE", L.GlobalStrategy.get_required_marks(), integers=True)
        #end if(ZeroLayer)
        
        if align and ( not L.get_ZeroLayer() ):
            s = add(s, "CORR_WAFER_GRID", Defaults.ProcessData_CORR_WAFER_GRID) # Usually above `NR_OF_Marks_TO_USE`
            s = add(s, "MIN_MARK_DISTANCE_COARSE", Defaults.ProcessData_MIN_MARK_DISTANCE_COARSE)
            s = add(s, "MIN_MARK_DISTANCE", Defaults.ProcessData_MIN_MARK_DISTANCE, integers=True)
            s = add(s, "MAX_80_88_SHIFT", Defaults.ProcessData_MAX_80_88_SHIFT)
            s = add(s, "MAX_MARK_RESIDUE", Defaults.ProcessData_MAX_MARK_RESIDUE)
            s = add(s, "SPM_MARK_SCAN", Defaults.ProcessData_SPM_MARK_SCAN)
            s = add(s, "ERR_DETECTION_88_8", Defaults.ProcessData_ERR_DETECTION_88_8)
        #end if(align)
        
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
        
        """ Appears that we can omit these without issue
            NUMERICAL_APERTURE                            0.570000
            SIGMA_OUTER                                   0.750000
        """            
        
        s = add(s, "RTCL_CHECK_SURFACES", Defaults.ProcessData_RTCL_CHECK_SURFACES)
        
        ## 3 ints:
        s = add(s, "RTCL_CHECK_LIMITS_UPPER", Defaults.ProcessData_RTCL_CHECK_LIMITS_UPPER, integers=True)
        s = add(s, "RTCL_CHECK_LIMITS_LOWER", Defaults.ProcessData_RTCL_CHECK_LIMITS_LOWER, integers=True)
        
        if align and ( not L.get_ZeroLayer() ):
            s = add(s, "ALIGNMENT_METHOD", Defaults.ProcessData_ALIGNMENT_METHOD)
        
        s = add(s, "CLOSE_GREEN_LASER_SHUTTER", Defaults.ProcessData_CLOSE_GREEN_LASER_SHUTTER)
        s = add(s, "REALIGNMENT_METHOD", Defaults.ProcessData_REALIGNMENT_METHOD)
        s = add(s, "IMAGE_ORDER_OPTIMISATION", Defaults.ProcessData_IMAGE_ORDER_OPTIMISATION)
        s = add(s, "RETICLE_ALIGNMENT", Defaults.ProcessData_RETICLE_ALIGNMENT)
        s = add(s, "USE_DEFAULT_RETICLE_ALIGNMENT_METHOD", Defaults.ProcessData_USE_DEFAULT_RETICLE_ALIGNMENT_METHOD)
        s = add(s, "CRITICAL_PERCENTAGE", Defaults.ProcessData_CRITICAL_PERCENTAGE, integers=True)
        s = add(s, "SHARE_LEVEL_INFO", Defaults.ProcessData_SHARE_LEVEL_INFO)
        s = add(s, "FOCUS_EDGE_CLEARANCE", Defaults.ProcessData_FOCUS_EDGE_CLEARANCE)
        
        if align and ( not L.get_ZeroLayer() ):
            s = add(s, "INLINE_Q_ABOVE_P_CALIBRATION", "M")
        else:
            s = add(s, "INLINE_Q_ABOVE_P_CALIBRATION", Defaults.ProcessData_INLINE_Q_ABOVE_P_CALIBRATION)
        
        s = add(s, "SHIFTED_MEASUREMENT_SCANS", Defaults.ProcessData_SHIFTED_MEASUREMENT_SCANS)
        s = add(s, "FOCUS_MONITORING", Defaults.ProcessData_FOCUS_MONITORING)
        s = add(s, "FOCUS_MONITORING_SCANNER", Defaults.ProcessData_FOCUS_MONITORING_SCANNER)
        s = add(s, "DYN_PERF_MONITORING", Defaults.ProcessData_DYN_PERF_MONITORING)
        s = add(s, "FORCE_MEANDER_ENABLED", Defaults.ProcessData_FORCE_MEANDER_ENABLED)
        s += "END_SECTION\n\n"
    # end for(LayerList)
    
    s += "\n\n\n\n\n"
    
    
    ################
    # Reticle Data #
    ################
    if DEBUG(): print("Generating Text Section 'RETICLE_DATA'...")
    for i,L in enumerate(JobObj.LayerList):
        if DEBUG(): print(   "  RETICLE_DATA: Layer %i, '%s'" % ( i, L.LayerID )   )
        for ii,I in enumerate(L.ImageList):
            if DEBUG(): print(   "    RETICLE_DATA: Image %i, '%s'" % ( ii, I.ImageID ), "\t[i=%i/ii=%i]"%(i,ii)   )
            s += "START_SECTION RETICLE_DATA\n"
            s = add(s, "LAYER_ID", L.LayerID)
            s = add(s, "IMAGE_ID", I.ImageID)
            s = add(s, "IMAGE_USAGE", "Y")
            s = add(s, "RETICLE_ID", I.ReticleID)
            s = add(s, "IMAGE_SIZE", I.get_ReticleSize() )
            s = add(s, "IMAGE_SHIFT", I.get_ReticleShift() )
            s = add(s, "MASK_SIZE", I.get_ReticleSize() )
            s = add(s, "MASK_SHIFT", I.get_ReticleShift() )
            s = add(s, "ENERGY_ACTUAL", L.EnergyList[ii] )
            s = add(s, "FOCUS_ACTUAL", L.FocusList[ii] )
            s = add(s, "FOCUS_TILT", L.FocusTiltList[ii] )
            s = add(s, "NUMERICAL_APERTURE", L.NAList[ii] )
            s = add(s, "SIGMA_OUTER", L.Sig_oList[ii] )
            if L.Sig_iList[ii]: s = add(s, "SIGMA_INNER", L.Sig_iList[ii] ) 
            s = add(s, "IMAGE_EXPOSURE_ORDER", 0, integers=True ) # IMAGE_EXPOSURE_ORDER 0
            s = add(s, "LITHOGRAPHY_PROCESS", L.IlluminationModeList[ii] )
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
    
    
    if DEBUG(): print("_genascii(): done generating ASCII string.")
    return s
#end _genascii()