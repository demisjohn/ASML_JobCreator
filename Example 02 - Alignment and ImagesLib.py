# -*- coding: utf-8 -*-
"""
ASML_JobCreator - Example 02
    Alignment and advanced options.
    Multi-layer job, multiple images per layer, with marks exposure and subsequent alignment to those marks.
    Also shows usage of predefined Images from files in ASML_JobCreator/Images/ directory.

@author: Demis D. John
Univ. of California Santa Barbara
UCSB Nanofabrication Facility: http://www.nanotech.ucsb.edu
2020-05-14


All units are in millimeters.  
Coordinates and sizes are specified as two-valued iterables like [X,Y]
All sizes and shifts are specified at 1x wafer-scale (NOT 4x/5x reticle-scale)

For help: after running once, use commands like:
    help( asml )
    help( MyJob )
    dir( MyJob.Cell )
    help( MyJob.Cell.set_CellSize )
"""

####################################################
# Module setup etc.

import ASML_JobCreator as asml

####################################################

print('Running...')

MyJob = asml.Job()

MyJob.set_comment("Demo Alignment Job", "", "Exported from Python ASML_JobCreator")


## Cell Structure:
MyJob.Cell.set_CellSize( [5.00, 5.00] )    # cell size [X,Y] in millimeters
MyJob.set_ExposeEdgeDie()  # Expose die that fall only partially on the wafer
MyJob.Cell.set_RoundEdgeClearance( 5 )  # Width of disallowed border of wafer
MyJob.Cell.set_FlatEdgeClearance( 3 )   # Width of disallowed border at wafer flat



## Image Definition:
#   MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)

## To expose on Layer 1:
#   Resolution test structures:
Res = MyJob.Image("UCSB_Res", "UCSB-OPC1", sizeXY=[3, 3], shiftXY=[4,5])

## To expose on Layer 2:
#   We'll use a pre-defined image from file, in the sub-folder ASML_JobCreator/Images/SPM_X.py
#   `dir( asml.Images )` will show you a list, or look inside the sub-folder.
#   You can place your own Image Library files into the Images subfolder.
#   We'll place X-scribe-line alignment marks, used as dicing alignment guides
DicingLine_X = MyJob.Image( asml.Images.SPM_X )  
# In order to use alignment mark images for other purposes, must give a custom Image ID, otherwise it thinks it's an SPM-X alignment mark:
DicingLine_X.set_ImageID( "DiceX" )



## Image Distribution
#   cellCR is integer pair of Col/Row specificiation
#   shiftXY is floating-point X/Y shift

## To expose on Layer 1:
# Distribute Image "Res" across whole wafer
for cells in MyJob.Cell.get_ValidCells():
    Res.distribute( cells )
#end for(cells)

## To expose on Layer 2:
# Distribute DicingX in rows across wafer, on top and bottom of cells:
for r in [-2,+1]:
    for c in range(-8,+9):
        DicingLine_X.distribute( [c,r], shiftXY=[0,+2.5] ) # top of cell
        DicingLine_X.distribute( [c,r], shiftXY=[0,+2.5] ) # bottom of cell
    #end for(c)
#end for(r)



## Alignment Mark Definition
E = MyJob.Alignment.Mark("E", "PM", waferXY=[42.5, 0.0])
EN = MyJob.Alignment.Mark("EN", "PM", waferXY=[42.5, 2.5])
ES = MyJob.Alignment.Mark("ES", "PM", waferXY=[42.5, -2.5])

W = MyJob.Alignment.Mark("W", "PM", waferXY=[-42.5, 0.0])
WN = MyJob.Alignment.Mark("WN", "PM", waferXY=[-42.5, 2.5])
WS = MyJob.Alignment.Mark("WS", "PM", waferXY=[-42.5, -2.5])

ALL = MyJob.Alignment.Strategy("ALL", marks=[E, EN, ES, W, WN, WS])
ALL.set_required_marks(2)    # num marks that must pass, defaults to all



## Layer Definition & Reticle Data - 
# Add Zero layer, with alignment mark exposure
ZeroLyr = MyJob.Layer()     # Empty blank Layer
ZeroLyr.set_ZeroLayer()     # Sets as special system-layer for alignment marks
ZeroLyr.expose_Marks(  marks=[E, EN, ES, W, WN, WS], Energy=21, Focus=-0.10  )   # set Marks Exposure. 

# Layer 1 - combine with Zero layer alignment mark exposure
Lyr1 = MyJob.Layer( LayerID="Lyr1" )
Lyr1.set_CombineWithZeroLayer()
Lyr1.expose_Image( Res, Energy=21, Focus=-0.10 )

# Layer 2 - Aligns to ZeroLayer
Lyr2 = MyJob.Layer( LayerID="Lyr2" )
Lyr2.set_PreAlignment( marks=[E, W] ) # choose 2 marks
Lyr2.set_GlobalAlignment( strategy=ALL )  # choose a global strategy
Lyr2.expose_Image( DicingLine_X, Energy=21, Focus=-0.10 )





# Print all the data added to this Job:
print(MyJob)
MyJob.Plot.plot_wafer()


## Export the text file:
asml.unset_WARN()   # Turn off warning messages about defaults
#   overwrite the file. A warning will be printed while doing so.
MyJob.export('Example02.txt', overwrite=True) 


print('done.')

