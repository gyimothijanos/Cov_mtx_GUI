'''
Created on 2015.12.10.

@author: Jani
@lector: Zoli
'''

"""
""""""
""""""""
Imports
""""""""
""""""
"""

import numpy as np
import copy


"""
""""""
""""""""
Functions
""""""""
""""""
"""

"""
Calculates the values of the Rarity vector from a given matrix.
"""
def getRarityVector(numberOfColumns, procSum):
	# rarity vector initialization
	rarityVector = [0] * numberOfColumns
	for colIndex in range (0, numberOfColumns):
		if procSum[colIndex] == 0:
			rarityVector[colIndex] = 0
		else:
			rarityVector[colIndex] = round((1 / (procSum[colIndex])), 2)
	return rarityVector	
	
"""
Creates Rarity matrix from given input matrix and rarity vector.
"""
def getRarityMatrix(input_matrix, rarityVector):
	(numberOfRows, numberOfColumns) = input_matrix.shape
	rarityMatrix = np.zeros((numberOfRows, numberOfColumns))
	for colIndex in range(0, numberOfColumns):
		for rowIndex in range(0, numberOfRows):
			if input_matrix[rowIndex, colIndex] == 1:
				rarityMatrix[rowIndex, colIndex] = rarityVector[colIndex]
	return rarityMatrix

"""
Creates the Test rarity vector, from given matrix and Rarity values.
"""
def getRarityTestVector(input_matrix, rarityMatrix, input_weight):
	(numberOfRows, numberOfColumns) = input_matrix.shape
	rarityTestVector = np.zeros(numberOfRows)
	for rowIndex in range(0, numberOfRows):    
		for colIndex in range(0, numberOfColumns):
			if input_matrix[rowIndex, colIndex] == 1:
				rarityTestVector[rowIndex] = rarityTestVector[rowIndex] + rarityMatrix[rowIndex, colIndex]    
	return rarityTestVector

"""
Creates a weighted average rarity matrix, then chooses the optimal test from it.
"""
def getWeightedRarityVector(testSum, rarityTestVector, input_weight):
	weightedRarityVector = []
	numberOfRows = len(rarityTestVector)
	if input_weight == 0:
		for rowIndex in range(0, numberOfRows):
			if testSum[rowIndex] == 0 or rarityTestVector.all == 0:
				weightedRarityVector.append(0)
			else:
				weightedRarityVector.append((testSum[rowIndex] / max(testSum) * (rarityTestVector[rowIndex] / max(rarityTestVector))) / (testSum[rowIndex] / max(testSum) + rarityTestVector[rowIndex] / max(rarityTestVector)))
	elif input_weight == 1:
		for rowIndex in range(0, numberOfRows):
			if testSum[rowIndex] == 0 or rarityTestVector.all == 0:
				weightedRarityVector.append(0)
			else:
				weightedRarityVector.append(rarityTestVector[rowIndex])
	return weightedRarityVector

"""
Selects a test based on the Weighted Rarity Vector.
"""
def selectTest(input_weight,testSum,weightedRarityVector):
	if input_weight == 0:
		rowIndex = 0
		finalSelections = []
		positionList = []
		maximumValue = max(testSum)
		for index in testSum:
			if index == maximumValue:
				positionList.append(rowIndex)
			rowIndex += 1
		position = positionList[0]
		for j in range(0, len(positionList)):
			if len(positionList) > 1 and weightedRarityVector[(positionList[j])] != 0:
				finalSelections.append(weightedRarityVector[(positionList[j])])
				position = weightedRarityVector.index(max(finalSelections))
			else:
				position = positionList[0]
	elif input_weight == 1:
		position = weightedRarityVector.index(max(weightedRarityVector))
	return position

"""
Simplifies the Rarity matrix and Rarity vector from a given test #way too much input parameter...
""" 
def simplifyMatrix1(input_matrix, rarityVector, rarityMatrix, rarityTestVector, position):
	(rows, cols) = input_matrix.shape
	for colIndex in range(0, cols):
		if input_matrix[position, colIndex] == 1:
			for rowIndex in range(0, rows):
				rarityTestVector[rowIndex] = round((rarityTestVector[rowIndex] - rarityMatrix[rowIndex, colIndex]), 2)
			rarityVector[colIndex] = 0
			rarityMatrix[:, colIndex] = 0
			for k in range(0, rows):
				input_matrix[k, colIndex] = 0
	return input_matrix

def simplifyMatrix2(input_matrix, input_weight, weightedRarityVector, testSum, rarityTestVector):
	(rows, cols) = input_matrix.shape
	if input_weight == 0:
		testSum = sum(input_matrix.T)
		# print("Tsum", testSum)
		for colIndex in range(0, rows):
			if testSum[colIndex] == 0 or rarityTestVector[colIndex] == 0:
				weightedRarityVector[colIndex] = 0    
	elif input_weight == 1:
		for colIndex in range(0, rows):
			if rarityTestVector[colIndex] == 0:
				weightedRarityVector[colIndex] = 0    
	return testSum
