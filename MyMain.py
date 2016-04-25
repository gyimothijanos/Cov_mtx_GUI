'''
Created on 2015.12.09.

@author: Jani
@lector: Zoli
'''

# Imports
from MyRarityAlgorithms import *
from MyClassicalAlgorithms import *
from MyConstants import *
from MyPlotter import *
import numpy as np
from MyInteractiveRun import *
from MyBuglocalizationAlgorithm import *
import os, fnmatch

"""
Running the program interactively in cmd with raw-inputs
"""
#interactiveRunner()


"""
TODO: Import and convert matrix
"""

"""
Global constans
"""
#numberOfRows=input_matrix.shape[0]
#numberOfCols=input_matrix.shape[1]
"""
Classical algorithms
"""
#classicAlg_WithDefaultParams(input_matrix)
#classicAlgWithOptimalization_WithDefaultParams(input_matrix)

"""
Rarity algorithms
"""
#rarityAlg_WithDefaultParams(input_matrix)
#rarityAlgWithOptimalization_WithDefaultParams(input_matrix) #if weight = 1 and we're running this specific algorithm there is an error in the code, yet to be solved#

"""
Plotter
"""
#Data for Histogram Plotter
#data = sum(input_matrix)

#histPlotter(data,binSize,binSizeType)
#ecdfPlotter(matrixSums,matrixRows,normValue,serialNumbersOfMatrices)