# -*- coding: utf-8 -*-
"""
ASML_JobCreator - Example 01
    Example usage, to export a text file for import into ASML PAS system.
    Multi-layer job, multiple images per layer, no alignments.

@author: Demis D. John
Univ. of California Santa Barbara
UCSB Nanofabrication Facility: http://www.nanotech.ucsb.edu
2020-01-18


All units are in millimeters.  
Coordinates and sizes are specified as two-valued iterables like [X,Y]

For help: after running once, use commands like:
    help( asml )
    help( MyJob )
    help( MyJob.Cell.set_CellSize )
"""

####################################################
# Module setup etc.

import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)

####################################################

print('Running...')


import ASML_JobCreator as asml
MyJob = asml.Job()

MyJob.set_comment("Demo Job", "Exported from ", "Python ASML_JobCreator")
print( MyJob.get_comment() )    # Return the current comment lines

## Cell Structure:
MyJob.Cell.set_CellSize( [4.00, 4.00] )    # cell size [X,Y] in millimeters
MyJob.Cell.set_MatrixShift( [2.00, 2.00] ) # shift by half a cell


## Image Definition:
#   MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)
#   see `help( MyJob.Image )`
Res = MyJob.Image("UCSB_Res", "UCSB-OPC1", sizeXY=[3, 3], shiftXY=[4,5])
MA6 = MyJob.Image("UCSB_MA6", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[-4,-5])
GCA = MyJob.Image("UCSB_GCA", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[0,-2])


## Image Distribution
#   cellCR is integer pair of Col/Row specificiation
#   shiftXY is floating-point X/Y shift
#   Add each of these to a single exposure location only:
MA6.distribute( cellCR=[-5,-5], shiftXY=[-2.00, -2.00] )
GCA.distribute( cellCR=[5,5], shiftXY=[-2.00, -2.00] )

# Distribute Image "Res" in a 3x3 array with no shift:
for r in range(3):
    for c in range(3):
        Res.distribute( [c,r] )
    #end for(c)
#end for(r)
print( Res )

MyJob.add_Images(Res,MA6, GCA)  # Add distributed images to our Job


## Layer Definition & Reticle Data - 
# Add Zero layer - possibly unnecessary for no alignment.
ZeroLyr = MyJob.Layer() # Empty Layer with default values
MyJob.add_Layers(ZeroLyr)

# Choose Images to expose on this Layer:
MetalLyr = MyJob.Layer( LayerID="Metal" )
MetalLyr.expose_Image(Res, Energy=21, Focus=-0.10)
MetalLyr.expose_Image(MA6, Energy=22)
MetalLyr.expose_Image(GCA, Energy=22)
MyJob.add_Layers(MetalLyr)  # Add these Images to the Layer


print(MyJob)

## Export the text file:
MyJob.export('TestJob_NoAlign.txt')


print('done.')
