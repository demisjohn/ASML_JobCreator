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

# import matplotlib.pyplot as plt – already done in globals.py

####################################################


class Plot(object):
    """
    Class to hold Plotting functions.
    """
    
    def __init__(self, parent=None):
        '''Create empty Plot object.'''
        self.parent = parent    # parent Job object
    #end __init__
    
    
    def plot_wafer(self):
        """
        Plot the Wafer layout and distributed Images.
        
        Returns
        -------
        fig, ax : Matplotlib Figure and Axis objects containing the plot.
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as mplp   # for plotting shapes
        import numpy as np
        
        fig, ax = plt.subplots(nrows=1, ncols=1)
        
        
        ## Plot the wafer outline:
        # Arc angles:
        F = self.parent.defaults.WFR_FLAT_LENGTH    # wafer flat length, mm
        D = self.parent.defaults.WFR_DIAMETER   # wafer diameter, mm
        A = np.rad2deg(  np.arcsin( (F/2) / (D/2) )  )  # arc angle corresponding to 1/2 of wafer flat
        # matplotlib.patches.Arc(xy, width, height, angle=0.0, theta1=0.0, theta2=360.0) :
        wf = mplp.Arc( (0,0) , D, D, angle=-90, theta1=A, theta2=-A , color='darkgrey', hatch='....')
        ax.add_patch( wf )
        
        
        ## Plot the edge clearance
        # Arc angles:
        Fc = F - self.parent.Cell.get_FlatEdgeClearance()
        Dc = D - 2*self.parent.Cell.get_RoundEdgeClearance()
        Ac = np.rad2deg(  np.arcsin( (Fc/2) / (Dc/2) )  )
        clearance = mplp.Arc( (0,0) , Dc, Dc, angle=-90, theta1=Ac, theta2=(-Ac) , color='lightgrey', hatch='....')
        ax.add_patch( clearance )
        
        
        ## Plot the Cell grid:
        def gen_grid(inc, maxval, shift=0):
            """Generate a 1-D grid around zero, up to +/- `maxval`, with `inc` between points.
            Returns 2 arrays:
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
            
            # shift grid by half-die, which is ASML default layout (with a die in wafer center)
            #major = major - inc/2
            
            if DEBUG(): print("gen_grid():", major, minor, index)
            return major, minor, index
        #end gen_grid()
                    
        CellSizeX = self.parent.Cell.CellSize[0]
        CellSizeY = self.parent.Cell.CellSize[1]
        CellShiftX = self.parent.Cell.get_MatrixShift()[0]
        CellShiftY = self.parent.Cell.get_MatrixShift()[1]
        
        gridx, mgridx, Ix = gen_grid(CellSizeX, D/2, shift= CellShiftX)
        gridy, mgridy, Iy = gen_grid(CellSizeY, D/2, shift= CellShiftY)
        
        
        # Plot grid, using Major grid for enumeration labels but no gridlines or ticks, and minor grid for gridlines and tick marks but no text-labels
        ax.set_xlabel("Cell Column")
        ax.set_ylabel("Cell Row")
        
        ax.set_xticks( gridx, minor=False )  # major tick locations
        ax.set_xticklabels(  [str(int(i)) for i in Ix]  )
        ax.set_xticks( mgridx, minor=True)  # minor tick locations
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
        #end for(xtick)
        
        ax.set_yticks( gridy, minor=False )
        ax.set_yticklabels(  [str(int(i)) for i in Iy]  )
        ax.set_yticks( mgridy, minor=True)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
        #end for(ytick)
        
        ax.grid(True, which='minor')
        ax.grid(False, which='major')
        
        
        # Plot the distributed images:
        cmap = plt.get_cmap("tab20")    # cycling colors
        LegendEntries = []
        for i, Img in enumerate(self.parent.ImageList):
            Iwidth = Img.sizeXY[0]
            Iheight = Img.sizeXY[1]
            for ii, Id in enumerate( Img.get_distribution() ):
                CellCR = Id[0]
                ShiftXY = Id[1]
                X = gridx[ list(Ix).index(CellCR[0]) ] + ShiftXY[0] - Iwidth/2
                Y = gridy[ list(Iy).index(CellCR[1]) ] + ShiftXY[1] - Iheight/2
                if DEBUG(): print("X,Y=", X,Y)
                Icen = np.array(  [ () , () ]  )
                # matplotlib.patches.Rectangle( (x,y), width, height):
                R = mplp.Rectangle( (X,Y),  Iwidth, Iheight, color=cmap(i), label=Img.ImageID )
                ax.add_patch(   R   )
                if ii==0: LegendEntries.append( R ) # add once only
            #end for(ImgDistr)
        #end for(Imagelist)
        
        # Shrink current axis by 20% for legend to fit
        box = ax.get_position()
        print("box=", box.x0, box.y0)   
        ax.set_position([box.x0 * 0.8, box.y0, box.width * 0.8, box.height])
        ax.axis('scaled')  # proportional axes

        # Put a legend to the right of the current axis
        ax.legend(handles=LegendEntries, loc='upper left', bbox_to_anchor=(1.01, 1), title="Images", borderaxespad=0.)
        
        fig.show()
        return fig, ax
    #end plot_wafer()
    
    def plot_reticle(self):
        """
        Plot the Reticle layout(s).  If multiple Reticle ID's are detected, multiple reticles will be plotted.
        """
        pass
    #end plot_wafer()
#end class(Plot)