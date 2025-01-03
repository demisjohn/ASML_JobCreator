# ASML_JobCreator
Python module to generate text job files for an [ASML PAS 5500/300 Stepper Lithography system](https://www.nanotech.ucsb.edu/wiki/index.php/Stepper_3_(ASML_DUV)), at the [UCSB Nanofabrication Facility](https://www.nanotech.ucsb.edu). A `Defaults.py` file can be created for your particular tool. Requires the relevant ASML Software options ("*Job Creator*") on the machine to convert the text output file into machine-usable files. 

Class heirarchy is set up similarly to the ASML *Job Definition* GUI.  The `Defaults.py` file, described below, may allow for usage on other ASML systems.

# Installation
- You must have access to an ASML tool that has the software option `JobCreator` (aka. JDJC or JC) installed, in order to convert the output of these scripts into binary job files.

- You must have a Python interpreter installed in order to use this module.  It is designed for use with Python 3.x. 
   - Common easy-to-install Scientific Python IDE's include [Anaconda Python](https://www.anaconda.com) > Spyder, or Jupyter Notebooks, or the command-line Python interpreter that is built-in to many operating sytems.
   
- **Download the latest _ASML_JobCreator_ package** at [GitHub > ASML_JobCreator > Releases](https://github.com/demisjohn/ASML_JobCreator/releases)
   - Extract the ZIP into a directory of your choice, and open/run an Example file with your Python IDE

- Obtain the `Defaults.py` file from your tool's manager - this file must be created using a text-exported job file from your tool.
   - UCSB users please see [this UCSB Nanofab wiki page](https://wiki.nanofab.ucsb.edu/wiki/ASML_Stepper_3_-_Job_Creator#Required_Files) to obtain this file.  Others may contact [the creator](mailto:demis@ucsb.edu) for advice on how to generate this file.
   - Place the `Defaults.py` file inside the `ASML_JobCreator/` subfolder.

# Usage

The following shows example usage, to export a text file via Python, for import into ASML PAS stepper system via `pas_recipe_import`.

Edit the appropriate *Example* file to your needs and execute the script with your Python interpreter.

The text file produced can be copied to your ASML PAS system.  On the system, execute the converter `pas_recipe_import` (with appropriate arguments) to generate the binary file that can be loaded into the PAS "*Job Definition*" GUI for further editing or the "*Task Streaming Queue*" for usage. Note that the text files must be placed in a specific directory on the system for the converter to locate them.

For help on a command: after importing module and creating Job object, use commands like:

    help( asml )
    help( MyJob )   # Print documentation on the object
    dir ( MyJob )   # Lists all available attributes
    help( MyJob.Cell.set_CellSize )

## Conventions

All units are in **millimeters**.  

Coordinates and sizes are specified as two-valued iterables like `[X,Y]`

All coordinates and sizes are specified at **1x wafer-scale** (not reticle 4x/5x scale).


## Examples of Syntax

    import ASML_JobCreator as asml
    MyJob = asml.Job()  # Create our Job object.

All info will be added to this `Job` object.  Commands like `help(MyJob)` or `dir(MyJob)` will show you available options and arguments.

`Set` and `Get` methods are defined for many operations.  The below comment line is optional - a default value will be provided for this and many other settings if left unspecified.

    MyJob.set_comment("Demo Job", "Exported from ", "Python ASML_JobCreator")
    print( MyJob.get_comment() )    # Return the current comment lines

### Cell Structure:

    MyJob.Cell.set_CellSize( [4.00, 4.00] )    # cell size [X,Y] in millimeters
    MyJob.Cell.set_MatrixShift( [2.00, 2.00] ) # shift the Cell Matrix by half a cell


### Image Definition: Define pattern location on printed reticle.
Arguments for adding an Image: 

&nbsp;&nbsp;&nbsp;&nbsp;`MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)`

see `help( MyJob.Image )` for full description of arguments.

    # Resolution Test Pattern:
    Res = MyJob.Image( "UCSB_Res", "UCSB-OPC1", sizeXY=[3.00, 3.00], shiftXY=[4.00, 5.00] )
    
    # MA6 Contact Alignment Mark:
    MA6 = MyJob.Image( "UCSB_MA6", "UCSB-OPC1", sizeXY=[2.00, 2.00], shiftXY=[-4.00, -5.00] )

#### Image Library: Easily store pre-defined Images
Predefined Images can be stored as simple text files in the [`/Images/` subfolder inside the module folder](https://github.com/demisjohn/ASML_JobCreator/tree/master/ASML_JobCreator/Images). Alignment Marks are already implemented using this Image library, see the files in the `/Image/` subfolder for examples.

### Image Distribution: Define wafer location of the above Images
A major benefit of python scripting: using nested `for` loops to place images across the wafer. Especially relevant to stitching images on varying pitches.

Arguments for distributing an Image on the wafer: 

&nbsp;&nbsp;&nbsp;&nbsp;`MyImage.distribute( cellCR=[Col,Row], shiftXY=[X_Shift, Y_shift] )`

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

### Alignment
[`Example02`](https://github.com/demisjohn/ASML_JobCreator/blob/master/Example%2002%20-%20Alignment%20and%20ImagesLib.py) shows an example of exposing and aligning to Alignment marks. Mark Images are predefined in the Image Library folder.

### Export the text file
    MyJob.export( 'TestJob_NoAlign.txt' )
    
The resulting text file can then be imported into the ASML PAS software as a binary job file, with the `pas_import_recipe` command-line tool.

### Plotting
Verify your wafer layouts or reticle layouts using the Plot commands:

`MyJob.Plot.plot_wafer()`:

<img src="https://user-images.githubusercontent.com/5370181/81465117-5f5b1b80-917c-11ea-91b3-b5b2c863384d.png" alt="plot_wafer()" width="450"/>
    
`MyJob.Plot.plot_reticles()`:

<img src="https://user-images.githubusercontent.com/5370181/81465151-a21cf380-917c-11ea-8b6d-415208376d75.png" alt="plot_reticles()" width="450"/>

## Default/System-Specific Settings

Default values for most options are specified in the file `ASML_JobCreator/Defaults.py`.  
You should be able to change these defaults to match your own system, using an exported text file from your system to populate the values.
For the UCSB Nanofab PAS 5500/300, defaults include settings such as:

- 100mm wafer with flat
- 6-inch reticle size
- 4x lens reduction (reticle magnification)
- default alignment methods 
- default edge exclusion zones etc. 

Some of these have `set`/`get` methods for manipulating them, others must be edited in the `Defaults.py` file.


## Drawbacks

This module is intended for users who already have experience programming their Jobs on the ASML PAS Job Definition GUI or a similar method.

The ASML Graphical Interface has many checks and tests built into the software to indicate if an invalid parameter has been entered.  This python script does not replicate the vast majority of those checks.  In practice, for very simple jobs this doesn't cause any problems.  However, for complex jobs (eg. stitching), this means that generating a new Job for the first time requires importing the job into the ASML to determine conversion errors, modifying the script and re-importing until errors have been removed.  Loading the converted job into the ASML Job Definition GUI is a good way to run the software checks.

# Author(s)

[Demis D. John](https://wiki.nanotech.ucsb.edu/wiki/index.php/Demis_D._John), Scientist at the [UCSB Nanofabrication Facility](http://www.nanotech.ucsb.edu), [Univ. of California Santa Barbara](http://www.ucsb.edu)
