# -*- coding: utf-8 -*-
"""
ASML_JobCreator - Example 03
    Grid of images and plotting examples.
    Several parts of the programming process are stream-lined using basic python objects.
    Also shows usage of predefined Images from files in ASML_JobCreator/Images/ directory.

@author: Ted Morin
Univ. of California Santa Barbara
UCSB Nanofabrication Facility: http://www.nanotech.ucsb.edu
2023-05-01


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

import matplotlib.pyplot as plt
import ASML_JobCreator as asml

####################################################

print('Running...')

MyJob = asml.Job()

MyJob.set_comment("Demo Grid Images Job", "", "Exported from Python ASML_JobCreator")


## Cell Structure:
MyJob.Cell.set_CellSize( [7.00, 6.00] )    # cell size [X,Y] in millimeters
MyJob.Cell.set_MatrixShift( [3.50, 3.00] ) # shift by half a cell
MyJob.unset_ExposeEdgeDie()  # set/unset (on/off) Expose die that fall only partially on the wafer
MyJob.Cell.set_RoundEdgeClearance( 0 )  # Width of disallowed border of wafer
MyJob.Cell.set_FlatEdgeClearance( 0 )   # Width of disallowed border at wafer flat

## Image Definition:
#   MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)

## define all images in a loop:
#   define images on the reticle in a grid
#   images are distributed below
layernames = ["LAY1", "LAY2", "LAY3"]
imagenames = ["A", "B", "C", "D"]
images = {}
for ii, layername in enumerate(layernames):
    for jj, imagename in enumerate(imagenames):
        fullname = layername+"_"+imagename
        images[fullname] = MyJob.Image(fullname, "MY_RETICLE", sizeXY=[6, 5],
            shiftXY=[(ii-1.5)*7.0+3.5, (jj-2)*6.0+3.0])

## Image Distribution
#   cellCR is integer pair of Col/Row specificiation
#   shiftXY is floating-point X/Y shift
#   distribution logi is implemented here
for xx, yy in MyJob.Cell.get_ValidCells():
    if xx < -6 or xx > 5: continue
    for fullname, image in images.items():
        if "LAY1_" in fullname or "LAY2_" in fullname:
            if "_A" in fullname and (xx%4 == 0): image.distribute( [xx, yy] )
            if "_B" in fullname and (xx%4 == 1): image.distribute( [xx, yy] )
            if "_C" in fullname and (xx%4 == 2): image.distribute( [xx, yy] )
            if "_D" in fullname and (xx%4 == 3): image.distribute( [xx, yy] )
        if "LAY3_" in fullname:
            if "_A" in fullname and (yy%4 == 0): image.distribute( [xx, yy] )
            if "_B" in fullname and (yy%4 == 1): image.distribute( [xx, yy] )
            if "_C" in fullname and (yy%4 == 2): image.distribute( [xx, yy] )
            if "_D" in fullname and (yy%4 == 3): image.distribute( [xx, yy] )

## Alignment Mark Definition
mark_dict = {
    "E" : MyJob.Alignment.Mark("E", "PM", waferXY=[42.5, 0.0]),
    "EN": MyJob.Alignment.Mark("EN", "PM", waferXY=[42.5, 2.5]),
    "ES": MyJob.Alignment.Mark("ES", "PM", waferXY=[42.5, -2.5]),
    "W" : MyJob.Alignment.Mark("W", "PM", waferXY=[-42.5, 0.0]),
    "WN": MyJob.Alignment.Mark("WN", "PM", waferXY=[-42.5, 2.5]),
    "WS": MyJob.Alignment.Mark("WS", "PM", waferXY=[-42.5, -2.5]),
}

ALL = MyJob.Alignment.Strategy("ALL", marks=mark_dict.values())
ALL.set_required_marks(2)    # num marks that must pass, defaults to all

# define layers in a loop
layers = {}
for ii, layername in enumerate(["zero"] + layernames):
    if ii == 0 :
        layers[layername] = MyJob.Layer()
        layers[layername].set_ZeroLayer()
        layers[layername].expose_Marks(marks = mark_dict.values(), Energy=21, Focus=-0.10)
    else :
        layers[layername] = MyJob.Layer(LayerID=layername)
        if ii == 1: layers[layername].set_CombineWithZeroLayer()
        else :
            layers[layername].set_PreAlignment( marks=[mark_dict["E"], mark_dict["W"]] ) # choose 2 marks
            layers[layername].set_GlobalAlignment( strategy=ALL )  # choose a global strategy

# expose images in a loop
for layername, layer in layers.items():
    if layername == "zero": continue
    for fullname, image in images.items():
        if layername in fullname:
            layer.expose_Image( image, Energy=21, Focus=-0.10 )

# Print all the data added to this Job:
print(MyJob)
# show plots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
MyJob.Plot.plot_wafer(figax=(fig, axes[1,0]), layer="LAY1"); axes[1,0].set_title("Layer 1")
MyJob.Plot.plot_wafer(figax=(fig, axes[0,1]), layer="LAY2"); axes[0,1].set_title("Layer 2")
MyJob.Plot.plot_wafer(figax=(fig, axes[1,1]), layer="LAY3"); axes[1,1].set_title("Layer 3")
axes[0,0].set_title("All layers")
MyJob.Plot.plot_wafer(figax=(fig, axes[0,0]),savewaferfig=True)
plt.tight_layout()
MyJob.Plot.plot_reticles(saveretfigs=True)
plt.show()

## Export the text file:
asml.unset_WARN()   # Turn off warning messages about defaults
asml.set_DEBUG()   # Turn on debugging output.
#   overwrite the file. A warning will be printed while doing so.
MyJob.export('examplejob03_grid_images.txt', overwrite=True) 


print('done.')

