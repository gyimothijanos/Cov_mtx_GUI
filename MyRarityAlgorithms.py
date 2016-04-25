'''
Created on 2015.12.10.

@author: Jani
@lector: Zoli
'''
from MyRarityUtils import *
from MyUtilities import *
from MyConstants import *
from tkinter import *
import tkinter as tk
from tkinter import messagebox


"""
Rarity alg. - default params.
"""
def rarityAlg_WithDefaultParams(input_matrix):   
	rarityAlgorithm(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)

"""
Rarity algorithm without pre algorithmic optimalization
"""
# Coverage matrix solving algorithm, using rarity values
def rarityAlgorithm(input_matrix, maxNumberOfTests, coverageRateToAchieve, input_weight):
	print("\nStarting rarity algorithm .....")
	
	
	work_matrix = copy.copy(input_matrix)
	#work_matrix = eliminateColumnsWithZeros(work_matrix)
	procSum = list(sum(work_matrix))
	numberOfUnexaminableColumns = procSum.count(0)
	
	(rows, columns) = work_matrix.shape
	testSum = sum(work_matrix.T)
	rarityVector = getRarityVector(columns, procSum)
	rarityMatrix = getRarityMatrix(work_matrix, rarityVector)
	rarityTestVector = getRarityTestVector(work_matrix, rarityMatrix, input_weight)
	weightedRarityVector = getWeightedRarityVector(testSum, rarityTestVector, input_weight)
	# prepare for starting the cycle
	sumCoverage = 0
	selectedTestPositions = []
	while (sumCoverage < coverageRateToAchieve) and (len(selectedTestPositions) < maxNumberOfTests) and sum(weightedRarityVector)!=0:
		position = selectTest(input_weight,testSum,weightedRarityVector)
		selectedTestPositions.append(position)
		work_matrix = simplifyMatrix1(work_matrix,rarityVector,rarityMatrix,rarityTestVector,position)
		testSum = simplifyMatrix2(work_matrix,input_weight,weightedRarityVector,testSum,rarityTestVector)
		sumCoverage = round(getCoverageOfThisMatrix(work_matrix,numberOfUnexaminableColumns),2)
	# Check if coverage is achieved or not
	if goal == 0:
		if (sumCoverage < coverageRateToAchieve):
			print("SUCCESSFUL:", sumCoverage, "% coverage rate has been reached in", maxNumberOfTests, " tests!")
		else:
			print("SUCCESSFUL:", coverageRateToAchieve, "% coverage rate has been reached with the given conditions!")
	else:
		print("SUCCESSFUL:","With the given conditions", sumCoverage,"% coverage rate has been achived!")
		
	# Print some info of the algorithm
	print("Actual coverage achieved by the algorithm:", sumCoverage, "%")
	print("Number of tests chosen by the algorithm:", len(selectedTestPositions))
	print("Positions of tests chosen by the algorithm:", selectedTestPositions)
	return selectedTestPositions,sumCoverage
	
"""
Rarity algorithm with pre algorithmic optimalization
"""

# Coverage matrix solving algorithm, using rarity values
def rarityAlgorithmWithOptimalization(input_matrix, maxNumberOfTests, coverageRateToAchieve, input_weight):
	print("\nStarting rarity algorithm with optimalization .....")

	work_matrix = copy.copy(input_matrix)
	#work_matrix = eliminateColumnsWithZeros(work_matrix)
	procSum = list(sum(work_matrix))
	numberOfUnexaminableColumns = procSum.count(0)

	selectedTestPositions = precoverageOptimalizationMatrix(work_matrix, maxNumberOfTests, coverageRateToAchieve)
	for index in range(0, len(selectedTestPositions)):
		work_matrix = simplifyThisMatrix(selectedTestPositions[index], work_matrix)
	(rows, columns) = work_matrix.shape
	procSum = sum(work_matrix)
	testSum = sum(work_matrix.T)
	rarityVector = getRarityVector(columns, procSum)
	rarityMatrix = getRarityMatrix(work_matrix, rarityVector)
	rarityTestVector = getRarityTestVector(work_matrix, rarityMatrix, input_weight)
	weightedRarityVector = getWeightedRarityVector(testSum, rarityTestVector, input_weight)
	sumCoverage = getCoverageOfThisMatrix(work_matrix,numberOfUnexaminableColumns)
	while (sumCoverage < coverageRateToAchieve) and (len(selectedTestPositions) < maxNumberOfTests) and sum(weightedRarityVector)!=0:
		# Select tests
		position = selectTest(input_weight,testSum,weightedRarityVector)
		selectedTestPositions.append(position)
		# refresh matrix
		work_matrix = simplifyMatrix1(work_matrix,rarityVector,rarityMatrix,rarityTestVector,position)
		testSum = simplifyMatrix2(work_matrix,input_weight,weightedRarityVector,testSum,rarityTestVector)
		sumCoverage = round(getCoverageOfThisMatrix(work_matrix,numberOfUnexaminableColumns),2)
	if goal == 0:
		if (sumCoverage < coverageRateToAchieve):
			print("SUCCESSFUL:", sumCoverage, "% coverage rate has been reached in", maxNumberOfTests, " tests!")
		else:
			print("SUCCESSFUL:", coverageRateToAchieve, "% coverage rate has been reached with the given conditions!")
	else:
		print("SUCCESSFUL:","With the given conditions", sumCoverage,"% coverage rate has been achived!")
		
		# Print some info of the algorithm
	print("Actual coverage achieved by the algorithm:", sumCoverage, "%")
	print("Number of tests chosen by the algorithm:", len(selectedTestPositions))
	print("Positions of tests chosen by the algorithm:", selectedTestPositions)
	return selectedTestPositions,sumCoverage
"""
Classical alg. with opt. - default params.
"""
def rarityAlgWithOptimalization_WithDefaultParams(input_matrix):   
	rarityAlgorithmWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
