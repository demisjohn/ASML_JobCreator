# ASML_JobCreator
Python module to generate text job files for an [ASML PAS 5500/300 Stepper Lithography system](https://www.nanotech.ucsb.edu/wiki/index.php/Stepper_3_(ASML_DUV)), at the [UCSB Nanofabrication Facility](https://www.nanotech.ucsb.edu). Requires the relevant ASML Software options ("*Job Creator*") on the machine to convert the text output file into machine-usable files.

Class heirarchy is set up similarly to the ASML *Job Definition* GUI.

# Example Usage

Example usage, to export a text file for import into ASML PAS stepper system via `pas_recipe_import`.

All units are in **millimeters**.  

Coordinates and sizes are specified as two-valued iterables like `[X,Y]`

For help: after importing module and creating Job object, use commands like:

    help( asml )
    help( MyJob )
    help( MyJob.Cell.set_CellSize )

## Examples of Syntax

    MyJob = asml.Job()  # Create our Job object.

All info will be added to this `Job` object.  Commands like `help(MyJob)` or `dir(MyJob)` will show you available options and arguments.

    MyJob.set_comment("Demo Job", "Exported from ", "Python ASML_JobCreator")
    print( MyJob.get_comment() )    # Return the current comment lines

`Set` and `Get` methods are defined for many operations.  The above comment line is optional - a default value is provided for many options.

### Cell Structure:

    MyJob.Cell.set_CellSize( [4.00, 4.00] )    # cell size [X,Y] in millimeters
    MyJob.Cell.set_MatrixShift( [2.00, 2.00] ) # shift by half a cell


### Image Definition: Define pattern location on printed reticle.
Arguments for adding an Image: `MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)`

see `help( MyJob.Image )` for full description of arguments.

    # Resolution Test Pattern:
    Res = MyJob.Image("UCSB_Res", "UCSB-OPC1", sizeXY=[3, 3], shiftXY=[4,5])
    
    # MA6 Contact Alignment Mark:
    MA6 = MyJob.Image("UCSB_MA6", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[-4,-5])


### Image Distribution: Define wafer location fo the above Images
Arguments for distributing an Image on the wafer: `MyImage.distribute( cellCR=[Col,Row], shiftXY=[X_Shift, Y_shift] )`

`cellCR` is integer pair of Col/Row specification

`shiftXY` is floating-point X/Y shift from cell center

    # Add Image "MA6" to a single exposure location only, offset from Cell center by 2x2mm:
    MA6.distribute( cellCR=[-5,-5], shiftXY=[-2.00, -2.00] )

    # Distribute Image "Res" in a 3x3 array with no shift:
    for r in range(3):
        for c in range(3):
            Res.distribute( [c,r] )
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
    MyJob.export('TestJob_NoAlign.txt')
    

The resulting text file can then be imported into the ASML PAS software as a binary job file, with the `pas_import_recipe` command-line tool.

# Author(s)

[Demis D. John](https://wiki.nanotech.ucsb.edu/wiki/index.php/Demis_D._John)

Scientist at the [UCSB Nanofabrication Facility](http://www.nanotech.ucsb.edu), [Univ. of California Santa Barbara](http://www.ucsb.edu)
