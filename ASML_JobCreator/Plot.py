"""
This file is part of the ASML_JobCreator package for Python 3.x.

plotting.py
    Plotting functions, for graphing wafers, reticles.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2020

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.

# import matplotlib.pyplot as plt # already done in globals.py

####################################################


class Plot(object):
    """
    Class to hold Plotting functions.
    """
    
    
    def __init__(self, parent=None):
        '''Create empty Plot object.'''
        self.parent = parent    # parent Job object
    #end __init__
    
    
    
    def plot_wafer(self, showwafer=True, showmarks=True):
        """
        Plot the Wafer layout and distributed Images.
        Note that some plotting options, such as font size and axis positioning, are set in __globals.py
        
        Parameters
        ----------
        showwafer, showmarks : True | False, optional
            Show the wafer outline marks + edge clearance (showware) and alignment marks (showmarks). Defaults to True.
        
        Returns
        -------
        fig, ax : Matplotlib Figure and Axis objects containing the schematic. Use these handles to manipulate the plot after generation. Matplotlib Patches are used to draw the shapes.
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as mplp   # for plotting shapes
        import numpy as np
        
        fig, ax = plt.subplots(nrows=1, ncols=1)
        LegendEntries = []
        
        ## Plot the wafer outline:
        # Arc angles:
        F = self.parent.defaults.WFR_FLAT_LENGTH    # wafer flat length, mm
        D = self.parent.defaults.WFR_DIAMETER   # wafer diameter, mm
        if Defaults.WFR_NOTCH.upper() == "N":
            A = np.rad2deg(  np.arcsin( (F/2) / (D/2) )  )  # arc angle corresponding to 1/2 of wafer flat
        else:
            A = 2
            
        if showwafer:
            # matplotlib.patches.Arc(xy, width, height, angle=0.0, theta1=0.0, theta2=360.0) :
            wf = mplp.Arc( (0,0) , D, D, angle=-90, theta1=A, theta2=-A , color=Defaults.Plotting_WaferEdgeColor, hatch=Defaults.Plotting_BGHatch, label="Edge Clearance")
            ax.add_patch( wf )
        
        
        ## Plot the edge clearance
        # Arc angles:
        Fc = F - self.parent.Cell.get_FlatEdgeClearance()
        Dc = D - 2*self.parent.Cell.get_RoundEdgeClearance()
        if Defaults.WFR_NOTCH.upper() == "N":
            Ac = np.rad2deg(  np.arcsin( (Fc/2) / (Dc/2) )  ) # arc angle corresponding to 1/2 of wafer flat
        else:
            Ac = 2
        
        if showwafer:
            clearance = mplp.Arc( (0,0) , Dc, Dc, angle=-90, theta1=Ac, theta2=(-Ac) , color=Defaults.Plotting_WaferColor, hatch=Defaults.Plotting_BGHatch, label="Wafer")
            ax.add_patch( clearance )
        
        
        ## Plot the Cell grid:
        def gen_grid(inc, maxval, shift=0):
            """Generate a 1-D grid around zero, up to +/- `maxval`, with `inc` between points.
            Returns 3 ndarrays:
                major : values at each grid point
                minor : values at minor grid, halfway between majors
                index : count at each grid point, with 0 in the middle.
            """
            major = np.arange(0, maxval, inc)
            index = np.array(   range( len(major) )   )
            # mirror both arrays:
            major = np.concatenate( (-1*np.flipud(major)[0:-1] , major) )  +  shift
            minor = np.concatenate( (major - inc/2, [major[-1] + inc/2]) )
            index = np.concatenate( (-1*np.flipud(index)[0:-1] , index) )
            if DEBUG(): print("gen_grid():", major, minor, index)
            return major, minor, index
        #end gen_grid()
                    
        CellSizeX = self.parent.Cell.CellSize[0]
        CellSizeY = self.parent.Cell.CellSize[1]
        CellShiftX = self.parent.Cell.get_MatrixShift()[0]
        CellShiftY = self.parent.Cell.get_MatrixShift()[1]
        
        # find max/min extents of distributed images:
        MaxX = MaxY = D/2
        for i, Img in enumerate(self.parent.ImageList):
            for ii, Id in enumerate( Img.get_distribution() ):
                CellCR = Id[0]
                #ShiftXY = Id[1]
                if np.abs(CellCR[0])*CellSizeX > MaxX: 
                    MaxX = np.abs(CellCR[0]) * CellSizeX
                if np.abs(CellCR[1])*CellSizeY > MaxY: 
                    MaxY = np.abs(CellCR[1]) * CellSizeY
            #end for(ImgDistr)
        #end for(ImageList)
        MaxX = MaxX + CellSizeX
        MaxY = MaxY + CellSizeY
        
        if DEBUG(): print("gen_grid(): MaxX, MaxY = ",MaxX, MaxY)
        
        gridx, mgridx, Ix = gen_grid(CellSizeX, MaxX, shift= CellShiftX)
        gridy, mgridy, Iy = gen_grid(CellSizeY, MaxY, shift= CellShiftY)
        
        
        # Plot grid, using Major grid for enumeration labels but no gridlines or ticks, and minor grid for gridlines and tick marks but no text-labels
        ax.set_xlabel("Cell Column", fontsize=PlotLabelFontSize)
        ax.set_ylabel("Cell Row", fontsize=PlotLabelFontSize)
        
        ax.set_xticks( gridx, minor=False )  # major tick locations
        ax.set_xticklabels(  [str(int(i)) for i in Ix], fontsize=PlotTickLabelSize )
        ax.set_xticks( mgridx, minor=True)  # minor tick locations
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
        #end for(xtick)
        
        ax.set_yticks( gridy, minor=False )
        ax.set_yticklabels(  [str(int(i)) for i in Iy], fontsize=PlotTickLabelSize )
        ax.set_yticks( mgridy, minor=True)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
        #end for(ytick)
        
        if showwafer:
            ax.grid(True, which='minor', color=Defaults.Plotting_GridColor, linestyle=Defaults.Plotting_GridStyle)
            ax.grid(False, which='major')
        #end if(showwafer)
        
                
        # Plot the distributed images:
        cmap = plt.get_cmap(Defaults.Plotting_ImageColorMap)    # cycling colors
        for i, Img in enumerate(self.parent.ImageList):
            Iwidth = Img.sizeXY[0]
            Iheight = Img.sizeXY[1]
            if Img.Layers:
                for ii, Id in enumerate( Img.get_distribution() ):
                    CellCR = Id[0]
                    ShiftXY = Id[1]
                    X = gridx[ list(Ix).index(CellCR[0]) ] + ShiftXY[0] - Iwidth/2
                    Y = gridy[ list(Iy).index(CellCR[1]) ] + ShiftXY[1] - Iheight/2
                    if DEBUG(): print("X,Y=", X,Y)
                    #DELETE? Icen = np.array(  [ () , () ]  )
                    # matplotlib.patches.Rectangle( (x,y), width, height):
                    R = mplp.Rectangle( (X,Y),  Iwidth, Iheight, color=cmap(i), label=Img.ImageID, alpha=Defaults.Plotting_Alpha, linewidth=Defaults.Plotting_LineWidth )
                    ax.add_patch(   R   )
                    if ii==0: LegendEntries.append( R ) # add once only
                #end for(ImgDistr)
            #end if(Img.Layers)
        #end for(Imagelist)
        
        
                # Plot alignment marks
        if self.parent.Alignment:
            cmap = plt.get_cmap(Defaults.Plotting_MarkColorMap)    # cycling colors
            c=-1 # colormap index
            AlImgs = []
            for i, Mrk in enumerate(self.parent.Alignment.MarkList):
                if DEBUG(): print("plot_wafer:marks(): MrkImg #%i:\n"%i, Mrk.Image.ImageID, "c=%i"%c   )
                Iwidth = Mrk.Image.sizeXY[0]
                Iheight = Mrk.Image.sizeXY[1]
                X = Mrk.waferXY[0] - Iwidth/2
                Y = Mrk.waferXY[1] - Iheight/2
                
                Imgi = np.where(   np.isin(AlImgs, Mrk.Image)  )[0]
                if len(Imgi)==0:
                    # Unlisted Mark Image
                    c = c+1 # cycle colormap
                #end if(Mark added to legend)
                
                R = mplp.Rectangle( (X,Y),  Iwidth, Iheight, 
                facecolor=Defaults.Plotting_MarkFace, 
                edgecolor=cmap(c),
                label=Mrk.Image.ImageID, 
                alpha=Defaults.Plotting_MarkAlpha, 
                linewidth=Defaults.Plotting_MarkLineWidth )
                ax.add_patch(   R   )
                
                if len(Imgi)==0:
                    # Unlisted Mark Image
                    AlImgs.append( Mrk.Image )
                    LegendEntries.append( R ) # add once only
                    if DEBUG(): print("plot_wafer:marks(): ", "\nAdding Legend entry %i\n"%len(LegendEntries), "MrkImg: ", Mrk.Image.ImageID, "c=%i"%c   )
                #end if(Mark added to legend)
            #end for(Imagelist)
        #end if(Alignment)
        
        
        # Shrink current axis by 20% for legend to fit
        box = ax.get_position()
        if DEBUG(): print("ax:box=", box.x0, box.y0)   
        ax.set_position([box.x0 * WaferPlotBox[0], box.y0 * WaferPlotBox[1], box.width * WaferPlotBox[2], box.height * WaferPlotBox[3]])
        ax.axis('scaled')  # proportional axes

        # Put a legend to the right of the current axis
        if showwafer:
            LegendEntries.extend( [clearance, wf] )
        ax.legend(handles=LegendEntries, title="Images", fontsize="small", loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0.)

        fig.show()
        return fig, ax
    #end plot_wafer()
    
    
    
    def plot_reticles(self, scale=False, showwindow=True, showlens=True):
        """
        Plot the Reticle layout(s).  If multiple Reticle ID's are detected, multiple reticles will be plotted.
        Note that some plotting options, such as font size and axis positioning, are set in __globals.py
        
        Parameters
        ----------
        scale : True | False, optional
            If True, plot at Reticle scale (eg. 4x or 5x, as set in `Defaults.py :: LENS_REDUCTION`).  Defaults to False, which plots at 1x wafer-scale.
            
        showwindow, showlens : True | False, optional
            If True, show the rectangular reticle table window (showwindow) and circular lens (showlens) outlines. These dimensions are defined in Defaults.py. Both defualt to True.
        
        Returns
        -------
        fig, ax : Lists of Matplotlib Figure and Axis objects containing the schematic. Use these handles to manipulate the plot after generation. Matplotlib Patches are used to draw the shapes.
        Each always returns a list, of length corresponding to the number of unique ReticleID's defined in the Job.
        """
        #if not DEBUG(): raise NotImplementedError("This function is incomplete!")
        
        if scale:
            Mag = Defaults.ProcessData_LENS_REDUCTION
        else:
            Mag = 1.0
        
        import matplotlib.pyplot as plt
        import matplotlib.patches as mplp   # for plotting shapes
        import numpy as np    
        
        Rets = self._get_ReticlesPerImage()
        figs, axs = [],[]        

        # set_DEBUG()
        for RetStr, Imgs in Rets.items():
            fig, ax = plt.subplots(nrows=1, ncols=1)
            figs.append(fig)
            axs.append(ax)
            LegendEntries = []
            
            if showlens:
                ## Plot the Lens outline:
                Lens = mplp.Circle( (0,0), Defaults.LENS_DIAMETER/2.0 * Mag, label="Lens Diameter", 
                facecolor=Defaults.Plotting_LensColor, 
                linewidth=Defaults.Plotting_ReticleBGOutlineWidth,
                edgecolor=Defaults.Plotting_ReticleBGOutlineColor, 
                linestyle=Defaults.Plotting_ReticleBGOutlineStyle,
                alpha = Defaults.Plotting_ReticleLensAlpha  )
                ax.add_patch(   Lens   )
            #end if(showlens)
        
            if showwindow:
                ## Plot the Reticle Table outline:
                RT = mplp.Rectangle( (-Defaults.RETICLE_TABLE_WINDOW[0]/2.0 * Mag, -Defaults.RETICLE_TABLE_WINDOW[1]/2.0 * Mag), Defaults.RETICLE_TABLE_WINDOW[0] * Mag, Defaults.RETICLE_TABLE_WINDOW[1] * Mag,
                label="Reticle Table Window", 
                facecolor=Defaults.Plotting_ReticleTableColor, 
                linewidth=Defaults.Plotting_ReticleBGOutlineWidth,
                edgecolor=Defaults.Plotting_ReticleBGOutlineColor, 
                linestyle=Defaults.Plotting_ReticleBGOutlineStyle,
                alpha = Defaults.Plotting_ReticleTableAlpha )
                ax.add_patch(   RT   )
            #end if(showwindow)
        
            ax.set_xlabel("%ix Scale, mm" % (Mag), fontsize=PlotLabelFontSize)
            ax.set_ylabel("mm", fontsize=PlotLabelFontSize)
            ax.set_title("ReticleID: " + RetStr)
            ax.grid(True, which='major', color=Defaults.Plotting_GridColor, linestyle=Defaults.Plotting_GridStyle)
        
            
            # Plot the defined images:
            cmap = plt.get_cmap(Defaults.Plotting_ImageColorMap)    # cycling colors
            for i, Img in enumerate(Imgs):
                #if DEBUG(): print("_get_ReticlesPerImage(): Imgs:\n", Imgs, "\nImg #%i\n"%i, Img)
                Iwidth = Img.sizeXY[0] * Mag
                Iheight = Img.sizeXY[1] * Mag
                X = Img.shiftXY[0] * Mag - Iwidth/2
                Y = Img.shiftXY[1] * Mag - Iheight/2
                
                R = mplp.Rectangle( (X,Y),  Iwidth, Iheight, color=cmap(i), label=Img.ImageID, alpha=Defaults.Plotting_Alpha, linewidth=Defaults.Plotting_LineWidth )
                ax.add_patch(   R   )
                LegendEntries.append( R ) # add once only
            #end for(Imagelist)
            
            
            # Shrink current axis by 20% for legend to fit
            box = ax.get_position()
            ax.set_position([box.x0 * WaferPlotBox[0], box.y0 * WaferPlotBox[1], box.width * WaferPlotBox[2], box.height * WaferPlotBox[3]])
            ax.axis('scaled')  # proportional axes

            # Put a legend to the right of the current axis
            if showlens:
                LegendEntries.append( Lens )
            if showwindow:
                LegendEntries.append( RT )
            ax.legend(handles=LegendEntries, title="Images", fontsize="small", loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0.)
        
            fig.show()
        #end for (RetStr)
        # unset_DEBUG()
        
        return figs, axs
    #end plot_wafer()
    
    plot_reticle = plot_reticles    # alias for convenience
    
    
    
    def _get_ReticlesPerImage(self):
        '''Analyze ReticleID's in each Image, and figure out how many reticles and which images are on it.
        
        Returns
        -------
        Reticles : list of strings
            Unique ReticleID's in this job
        Images : list of lists
            Each list corresponds to the Reticle ID.
        
        Examples
        --------
        >>> One = Image(ImageID="One", ReticleID="Ret1", ....)
        >>> Two = Image(ImageID="Two", ReticleID="Ret1", ....)
        >>> Three = Image(ImageID="Three", ReticleID="RetTwo", ....)
        >>> Reticles = _get_ReticlesPerImage( [One, Two, Three] )
        returns:
        : Reticles = {"Ret1" : [One,Two] , "RetTwo": [Three]}
        '''
        Rets = {}
        for I in self.parent.ImageList:
            Rstr = I.get_ReticleID()
            if Rstr in Rets: Rets[Rstr].append(I)
            else: Rets[Rstr] = [I]
        #end for(ImageList)
        if DEBUG(): print("_get_ReticlesPerImage(): Rets = \n", Rets)
        return Rets
    #end _get_ReticlesPerImage()
        
#end class(Plot)
