'''
Created on 2015.12.10.

@author: Jani
@lector: Zoli
'''


import numpy as np


# demo input matrix
#demo_input_matrix = np.array([[1, 1, 0, 1], [1, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 1]])

# import matrix location
import_matrix_location = "C:\munka\Cov_Mtx_Benchmark\Originals\oryx.jacoco.csv"

# Define coverage rate to achieve (in percents)
coverageRateToAchieve = 100

# Define how many tests should be selected at most
maxNumberOfTests = 50

# Weight 
#weight = 1

# Goal of the algorithm: If 0 => we are searching for the number of tests needed to achive the desired coverage rate. If it's 1 => we're searching for the coverage rate achived by the given number of maximal chosen test.
goal = 0

#normalizationValue: If 0=> There will be no norming in the plotting, if 1=> the graphs will be normed to x axis, if 2=> the graphs will be normed to y axis, if 3=> the graphs will be normed to both x and y axises. 
#normValue = 3

#Serial number of plotted matrices.
#serialNumbersOfMatrices = [0,1,2,4]

#Type of choosing binsize. If 0=> automatic binsize, if 1=> manually set binsize (binSize constant).
#binSizeType=0

#Value of manually set binsize.
binSize=100

