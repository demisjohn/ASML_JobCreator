# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

####################################################
# Module setup etc.

import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax

#import scipy as sp  # SciPy (signal and image processing library)
#import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
#from pylab import *              # Matplotlib's pylab interface
plt.ion()                         # Turn on Matplotlib's interactive mode

# More modules
import time                       # Get current date/time

####################################################

print('Running...')


import ASML_JobCreator as asml
MyJob = asml.Job()

print( MyJob.get_comment() )
MyJob.set_comment("Test Job", "Line2", "Line3")
print( MyJob.get_comment() )    

MyJob.Cell.set_CellSize( [4,4] )

MyJob.Cell.set_MatrixShift( [2,2] ) # defaults

Res = MyJob.Image("UCSB_Res", "UCSB-OPC1", sizeXY=[3, 3], shiftXY=[4,5])
MA6 = MyJob.Image("UCSB_MA6", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[-4,-5])
GCA = MyJob.Image("UCSB_GCA", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[0,-2])

MA6.distribute( cellCR=[-5,-5], shiftXY=[-2,-2] )
GCA.distribute( cellCR=[5,5], shiftXY=[-2,-2] )

for r in range(10):
    for c in range(10):
        Res.distribute( [c,r] )
    #end for(c)
#end for(r)
print( Res )

MyJob.add_Images(Res,MA6)

ZeroLyr = MyJob.Layer()
MyJob.add_Layers(ZeroLyr)


MetalLyr = MyJob.Layer( LayerID="Metal" )
MetalLyr.expose_Image(Res, Energy=21, Focus=-0.10)
MetalLyr.expose_Image(MA6, Energy=22)
MetalLyr.expose_Image(GCA, Energy=22)
MyJob.add_Layers(MetalLyr)


print(MyJob)

MyJob.export('testoutput.txt')





print('done.')



