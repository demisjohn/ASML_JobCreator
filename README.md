# ASML_JobCreator
Python module to generate text job files for an [ASML PAS 5500/300 Stepper Lithography system](https://www.nanotech.ucsb.edu/wiki/index.php/Stepper_3_(ASML_DUV)), at the [UCSB Nanofabrication Facility](https://www.nanotech.ucsb.edu). Requires the relevant ASML Software options ("*Job Creator*") on the machine to convert the text output file into machine-usable files.

Class heirarchy is set up similarly to the ASML *Job Definition* GUI.

# Installation

You must have a Python interpreter installed in order to use this module.  It is designed for use with Python 3.x, although 2.x may work (untested). 

Common easy-to-install Scientific Python IDE's include [Anaconda Python](https://www.anaconda.com) > Spyder, or Jupyter Notebooks, or the command-line Python interpreter that is built-in to many modern operating sytems.

Download the latest ASML_JobCreator package from [GitHub/ASML_JobCreator/Releases](https://github.com/demisjohn/ASML_JobCreator/releases), and extract into a directory of your choice.  

Edit the *Example* file to your needs and execute the script with your Python interpreter.

The text file produced can be copied to your ASML PAS system.  On the system, execute the converter `pas_recipe_import` (with appropriate arguments) to generate the binary file that can be loaded into the PAS "*Job Definition*" GUI for further editing or the "*Task Streaming Queue*" for usage.

# Usage

Example usage, to export a text file for import into ASML PAS stepper system via `pas_recipe_import`.

All units are in **millimeters**.  

Coordinates and sizes are specified as two-valued iterables like `[X,Y]`

For help on a command: after importing module and creating Job object, use commands like:

    help( asml )
    help( MyJob )
    help( MyJob.Cell.set_CellSize )

## Examples of Syntax

    MyJob = asml.Job()  # Create our Job object.

All info will be added to this `Job` object.  Commands like `help(MyJob)` or `dir(MyJob)` will show you available options and arguments.

`Set` and `Get` methods are defined for many operations.  The below comment line is optional - a default value will be provided for this and many other settings if left unspecified.

    MyJob.set_comment("Demo Job", "Exported from ", "Python ASML_JobCreator")
    print( MyJob.get_comment() )    # Return the current comment lines

### Cell Structure:

    MyJob.Cell.set_CellSize( [4.00, 4.00] )    # cell size [X,Y] in millimeters
    MyJob.Cell.set_MatrixShift( [2.00, 2.00] ) # shift by half a cell


### Image Definition: Define pattern location on printed reticle.
Arguments for adding an Image: 

&nbsp;&nbsp;&nbsp;`MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)`

see `help( MyJob.Image )` for full description of arguments.

    # Resolution Test Pattern:
    Res = MyJob.Image( "UCSB_Res", "UCSB-OPC1", sizeXY=[3.00, 3.00], shiftXY=[4.00, 5.00] )
    
    # MA6 Contact Alignment Mark:
    MA6 = MyJob.Image( "UCSB_MA6", "UCSB-OPC1", sizeXY=[2.00, 2.00], shiftXY=[-4.00, -5.00] )


### Image Distribution: Define wafer location of the above Images
Arguments for distributing an Image on the wafer: 

&nbsp;&nbsp;&nbsp;`MyImage.distribute( cellCR=[Col,Row], shiftXY=[X_Shift, Y_shift] )`

`cellCR` is integer pair of Col/Row specification

`shiftXY` is floating-point X/Y shift from cell center

    # Add Image "MA6" to a single exposure location only, offset from Cell center by 2x2mm:
    MA6.distribute( cellCR=[-5, -5], shiftXY=[-2.00, -2.00] )

    # Distribute Image "Res" in a 3x3 array with no shift:
    for r in range(3):
        for c in range(3):
            Res.distribute( [c,r] )     # 1st arg is `cellCR`. shiftXY defaults to (0,0)
        #end for(c)
    #end for(r)
    
    print( Res )    # print Image Def/Dist. info to the console

### Layer Definition & Reticle Data
Make a new layer, and choose which Images get exposed on it:

    MetalLyr = MyJob.Layer( LayerID="Metal" )
    MetalLyr.expose_Image(Res, Energy=21, Focus=-0.10)
    MetalLyr.expose_Image(MA6, Energy=22)

    print(MyJob)    # Print all info about this Job, including Images, Layers etc.

### Export the text file:
    MyJob.export( 'TestJob_NoAlign.txt' )
    
The resulting text file can then be imported into the ASML PAS software as a binary job file, with the `pas_import_recipe` command-line tool.

## Defaults

Default values for most options are specified in the file `ASML_JobCreator/Defaults.py`.  For the UCSB Nanofab PAS 5500/300, this includes settings such as 100mm wafer with flat, 6-inch reticle size, default alignment methods and edge exclusion zones etc. Some of these have `set`/`get` methods for manipulating them.

# Author(s)

[Demis D. John](https://wiki.nanotech.ucsb.edu/wiki/index.php/Demis_D._John), Scientist at the [UCSB Nanofabrication Facility](http://www.nanotech.ucsb.edu), [Univ. of California Santa Barbara](http://www.ucsb.edu)
