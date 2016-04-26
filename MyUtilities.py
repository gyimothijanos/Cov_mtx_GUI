'''
Created on 2015.12.09.

@author: Jani
@lector: Zoli
'''

"""
Imports
"""
import os
import heapq
import numpy as np
import random as rnd
import copy
import time
import numpy as np
import random as rnd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from numpy import genfromtxt
import pandas as pd
from pandas import DataFrame
import csv
import math
from MyPlotter import *


"""
Functions
"""


""" 
Fills a vector of given size with 1-s with the given probability.
""" 
def approxFill(size, probability):
	if probability < 0 or probability > 1:
		print("The probability value is not correct! It should be between 0 and 1")
		return
	else:
		vector = np.zeros(size)
		for index in range(0, len(vector)):
			if rnd.randint(1, size) <= int(size * probability):
				vector[index] = 1
			else:
				vector[index] = 0
		return vector
	
"""
Creates a Matrix of given size filled with 1-s, with given probability (using approxFill function).
"""
def createCoverageMatrix(numberOfRows, numberOfColumns, probability):
	matrixShape = (numberOfRows, numberOfColumns)
	
	coverageMatrix = np.zeros(shape = matrixShape)
	for rowIndex in range(0, numberOfRows):
		coverageMatrix[rowIndex] = approxFill(numberOfColumns, probability)
	
	# return with the coverage matrix
	return coverageMatrix

"""
Converts a given "rawMatrix" (created from CSV) to a output_matrix with np.matrx format, which we can use later on.
"""
def getConvertedMatrix(rawCSVMmatrix):
	temporaryMatrix=np.zeros(shape=(rawCSVMmatrix.shape[0],(len(rawCSVMmatrix[0][0])+1)/2))
	print("Shape of the matrix:", temporaryMatrix.shape)
	for index in range(len(rawCSVMmatrix)):
			newrow=list(map(int, rawCSVMmatrix[index,0].split(';')))
			temporaryMatrix[index] = np.asarray(newrow)
	output_matrix=temporaryMatrix.astype(int)
	return output_matrix

"""
Shows the relative coverage value (in percentage) of a given matrix.
"""     
def getCoverageOfThisMatrix(matrix, numberOfUnexaminableColumns):
	numberOfColumns = matrix.shape[1]
	procSum = list(sum(matrix))
	numberOfAllZeroColumns = procSum.count(0)
	return (numberOfAllZeroColumns-numberOfUnexaminableColumns) / numberOfColumns * 100
	
"""
Generates a random set of tests
"""
def randomTestGenerator(input_matrix,numberOfTests):
	randomlySelectedTests = rnd.sample(range(0,input_matrix.shape[0]), numberOfTests)
	return randomlySelectedTests
	
""" 
Deletes all columns of a given matrix, in which there are no 1-s (they cannot be examined by any of the tests).
"""
def eliminateColumnsWithZeros(input_matrix):
	print("Starting to eliminate columns...")
	indexesOfColumnsToRemove = []
	# counts the sum of the columns and returns as a vector
	sumOfColumns = (sum(input_matrix))
	# count removed column indexes
	for colIndex in range(0, input_matrix.shape[1]):
		if sumOfColumns[colIndex] == 0:
			indexesOfColumnsToRemove.append(colIndex)

	output_matrix = np.delete(input_matrix, indexesOfColumnsToRemove, 1)
	
	if (len(indexesOfColumnsToRemove) > 0):
		print("Selected columns to eliminate:", indexesOfColumnsToRemove)
	else:
		print("No columns have been eliminated!")
	return output_matrix

"""
Simplifies the matrix after selecting a test.
"""
def simplifyThisMatrix(selectedTestPosition, input_matrix):
	output_matrix = copy.copy(input_matrix)
	numberOfColumns = input_matrix.shape[1]
	for colIndex in range(0, numberOfColumns):
		if output_matrix[selectedTestPosition, colIndex] != 0:
			output_matrix[:, colIndex] = 0
	return output_matrix

"""
It does an optimalization by choosing necessary test before the coverage algorithm starts .
"""
def precoverageOptimalizationMatrix(input_matrix, maxNumberOfTests, coverageToAchieve):
	print("Starting the reduction algorithm...")
	
	procSum = list(sum(input_matrix))
	numberOfUnexaminableColumns = procSum.count(0)
	
	iteration = 0
	sumCoverage = 0
	coverageList = []
	testPositions = []
	while (1 in procSum) and (iteration < maxNumberOfTests) and (sumCoverage<coverageToAchieve):
		t = (input_matrix[:, procSum.index(1)]).tolist()
		rowPosition = t.index(1)
		testPositions.append(rowPosition)
		
		input_matrix = simplifyThisMatrix(rowPosition, input_matrix)
		sumCoverage = round(getCoverageOfThisMatrix(input_matrix,numberOfUnexaminableColumns),2)
		coverageList.append(sumCoverage)
		
		iteration = iteration + 1
		procSum = list(sum(input_matrix))

	if iteration != 0:
		print("Number of tests chosen by reduction:", len(testPositions))
		print("Position of tests chosen by reduction:", testPositions)
	if numberOfUnexaminableColumns != 0:
		print("Real coverage achieved by the algorithm:", sumCoverage, "%")
	else:	
		print("Relative coverage achieved by the algorithm:", sumCoverage, "%")
	print("End of reduction")
	return testPositions

"""
Calculates the maximal possible coverage for the input matrix.
"""
def maximalCoverageCalculator(input_matrix):
	numberOfColumns = input_matrix.shape[1]
	procSum = list(sum(input_matrix))
	numberOfAllZeroColumns = procSum.count(0)
	return (numberOfColumns-numberOfAllZeroColumns) / numberOfColumns * 100
	
	
