'''
Created on 2015.12.10.

@author: Jani
@lector: Zoli
'''

from MyBuglocalizationUtilities import *
from MyUtilities import *
from MyConstants import *
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import messagebox

"""
Collects the positions of tests that has the maximum value of testsum and returns the first one of these.
""" 
def selectTest(testsum):
	maxValue = max(testsum)
	result = np.where(testsum == maxValue)
	return result[0][0]

"""
I. Classical algorithm without pre_alg_opt#
"""
def classicAlg(input_matrix, maxNumberOfTests, coverageRateToAchieve):
	print("\nStarting classical algorithm .....")

	work_matrix = copy.copy(input_matrix)
	#work_matrix = eliminateColumnsWithZeros(input_matrix)

	procSum = list(sum(work_matrix))
	numberOfUnexaminableColumns = procSum.count(0)
		
	# prepare for starting the cycle
	sumCoverage = 0
	selectedTestPositions = []
	while (sumCoverage < coverageRateToAchieve) and (len(selectedTestPositions) < maxNumberOfTests):
		if np.count_nonzero(work_matrix) == 0:
			print("SUCCESSFUL:", "There are no more tests to select!")
			break
		else:
			# sum of rows
			testCoverage = sum(work_matrix.T)

			# select test, with maximal value
			position = selectTest(testCoverage)
			selectedTestPositions.append(position)
			# new input matrix (simplify the old one)
			#print(sum(sum((work_matrix))))
			work_matrix = simplifyThisMatrix(position, work_matrix)
			#print(sum(sum((work_matrix))))			
			sumCoverage = round(getCoverageOfThisMatrix(work_matrix,numberOfUnexaminableColumns),2)
			
	# Check if coverage is achieved or not
	#if goal == 0:
	#	if (sumCoverage < coverageRateToAchieve):
			#print("SUCCESSFUL:", sumCoverage, "% coverage rate has been reached in", maxNumberOfTests, " tests!")
	#	else:
			#print("SUCCESSFUL:", coverageRateToAchieve, "% coverage rate has been reached with the given conditions!")
	#else:
		#print("SUCCESSFUL:","With the given conditions", sumCoverage,"% coverage rate has been achived!")
		
	# Print some info of the algorithm
	if numberOfUnexaminableColumns != 0:
		print("Real coverage achieved by the algorithm:", sumCoverage, "%")
	else:	
		print("Relative coverage achieved by the algorithm:", sumCoverage, "%")
	#print("Number of tests chosen by the algorithm:", len(selectedTestPositions))
	print("Positions of tests chosen by the algorithm:", selectedTestPositions)
	return selectedTestPositions,sumCoverage

"""
Classical alg. - default params.
"""
def classicAlg_WithDefaultParams(input_matrix):   
    classicAlg(input_matrix, maximumNumberOfTests, coverageToAchieve)

"""
II. Classical algorithm with pre_alg_opt#
"""
def classicalAlgWithOptimalization(input_matrix, maxNumberOfTests, coverageRateToAchieve):                                
	print("\nStarting classical algorithm with optimalization .....")
	
	
	work_matrix = copy.copy(input_matrix)
	#work_matrix = eliminateColumnsWithZeros(input_matrix)
	
	procSum = list(sum(work_matrix))
	numberOfUnexaminableColumns = procSum.count(0)
	
	# pre coverage optimalization
	selectedTestPositions = precoverageOptimalizationMatrix(input_matrix, maxNumberOfTests, coverageRateToAchieve)
	for index in range(0, len(selectedTestPositions)):
		# Simplify matrix
		input_matrix = simplifyThisMatrix(selectedTestPositions[index], input_matrix)

	# Get current coverage
	sumCoverage = getCoverageOfThisMatrix(input_matrix,numberOfUnexaminableColumns)

	while (sumCoverage < coverageRateToAchieve) and (len(selectedTestPositions) < maxNumberOfTests):
		if np.count_nonzero(input_matrix) == 0:
			print("SUCCESSFUL:", "There are no more tests to select!")
			break
		else:
			# sum of rows
			testCoverage = sum(input_matrix.T)
			
			# select test, with maximal value
			position = selectTest(testCoverage)
			selectedTestPositions.append(position)
	
			# new input matrix (simplify the old one)
			input_matrix = simplifyThisMatrix(position, input_matrix)
			sumCoverage = round(getCoverageOfThisMatrix(input_matrix,numberOfUnexaminableColumns),2)
	
	# Check if coverage is achieved or not
	if goal == 0:
		if (sumCoverage < coverageRateToAchieve):
			print("SUCCESSFUL:", sumCoverage, "% coverage rate has been reached in", maxNumberOfTests, " tests!")
		else:
			print("SUCCESSFUL:", coverageRateToAchieve, "% coverage rate has been reached with the given conditions!")
	else:
		print("SUCCESSFUL:","With the given conditions", sumCoverage,"% coverage rate has been achived!")
		
	# Print some info of the algorithm
	if numberOfUnexaminableColumns != 0:
		print("Real coverage achieved by the algorithm:", sumCoverage, "%")
	else:	
		print("Relative coverage achieved by the algorithm:", sumCoverage, "%")
	print("Actual coverage achieved by the algorithm:", sumCoverage, "%")
	print("Number of tests chosen by the algorithm:", len(selectedTestPositions))
	print("Positions of tests chosen by the algorithm:", selectedTestPositions)
	return selectedTestPositions,sumCoverage
	
"""
Classical alg. with opt. - default params.
"""
def classicAlgWithOptimalization_WithDefaultParams(input_matrix):   
	classicalAlgWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve)

def coverageRateForChosenTests(input_matrix, selectedTests):
	work_matrix = copy.copy(input_matrix)
	#work_matrix = eliminateColumnsWithZeros(input_matrix)
	procSum = list(sum(work_matrix))
	numberOfUnexaminableColumns = procSum.count(0)
	
	for position in(selectedTests):
		work_matrix = simplifyThisMatrix(position, work_matrix)
	sumCoverage = round(getCoverageOfThisMatrix(work_matrix, numberOfUnexaminableColumns),2)
	print(sumCoverage)
	return sumCoverage

