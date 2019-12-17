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




print('done.')



