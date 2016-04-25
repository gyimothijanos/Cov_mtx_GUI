"""
Created on 2016.02.01.

@author: Jani
"""

import itertools
from MyUtilities import * 
from MyBuglocalizationUtilities import *

"""
Input Matrices
"""

#print("Size of Null Partition:", (sum(input_matrix).tolist()).count(0),"\n")
#input_matrix=eliminateColumnsWithZeros(input_matrix)
#input_matrix = np.array([[0,1,0,1,1,0,0,1],[1,1,0,0,1,1,1,0],[0,1,0,0,1,1,0,0],[0,0,0,1,0,0,1,1]])
#input_matrix = np.array([[1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0],[1,0,0,0,0,1,0,1,1,0,1,1,0,1,0,0],[0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,0],[0,1,0,1,1,0,1,1,0,1,0,0,1,0,1,1],[0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,0,1,0,0,1,1,0,1,0,0,1,0,1,1]])

"""
Breaking conditions
"""
#flRateToAchieve = 0.0
#maxNumberOfTests = 5

"""
In each cycle the algorithm chooses the test with the best metrical participation.
"""
def optimalBugLocalizationAlgorithm(input_matrix,maxNumberOfTests, flRateToAchieve):
	print("Starting optimal buglocalization algorithm...")
	(numberOfRows,numberOfCols) = input_matrix.shape
	work_matrix = copy.copy(input_matrix)
	selectedTests = []
	borderList = [0,input_matrix.shape[1]]
	localizationValue = 1
	indexTable = np.asarray(list(range(0,input_matrix.shape[0])))
	while len(selectedTests)<maxNumberOfTests and len(selectedTests)<numberOfRows and localizationValue>flRateToAchieve:
		numberOfCols = work_matrix.shape[1]
		index = len(selectedTests)
		minimum = 1
		for i in range(index,work_matrix.shape[0]):
			newBorders=[]
			for j in range(len(borderList)-1):
				currentSum=sum(work_matrix[i,borderList[j]:borderList[j+1]])
				if currentSum == 0 or  currentSum == (borderList[j+1]-borderList[j]):
					pass
				else:
					newBorders.append(borderList[j+1]-currentSum)
			current=evaluator(sorted(borderList+newBorders),numberOfCols)
			if current<minimum:
				minimum=current
				borders=newBorders
				position=i
		localizationValue = minimum
		indexTable[index:position+1]=np.roll(indexTable[index:position+1],1,0)
		work_matrix[index:position+1,:]=np.roll(work_matrix[index:position+1,:],1,0)
		for i in range(len(borderList)-1):
			work_matrix[ index:,borderList[i]: borderList[i+1]]=work_matrix[ index:, borderList[i]: borderList[i+1]][:,np.argsort(work_matrix[index, borderList[i]:borderList[i+1]])]
		selectedTests.append(indexTable[index])
		borderList=sorted(borderList+borders)
		#work_matrix,borderList=eliminateOnePartitions(borderList,work_matrix)
	localizationValue=round(evaluator(borderList,numberOfCols),2)
	print("Fl Opt metric:", localizationValue)
	return localizationValue, selectedTests

"""
In each cycle the algorithm choses p (p = number of partitions) tests, in such a way, that each test has the best metrical participation in it's partition.
"""
def fastBugLocalizationAlgorithm(input_matrix,maxNumberOfTests, flRateToAchieve):
	print("Starting Fast buglocalization algorithm...")
	(numberOfRows,numberOfCols) = input_matrix.shape
	work_matrix = copy.copy(input_matrix)
	borderList = [0,input_matrix.shape[1]]
	localizationValue = 1
	selectedTests = []
	indexTable = np.asarray(list(range(0,input_matrix.shape[0])))
	while len(selectedTests)<maxNumberOfTests and len(selectedTests)<numberOfRows and localizationValue>flRateToAchieve:
		newPositions = []
		index = len(selectedTests)
		for j in range(len(borderList)-1):
			minimum = 1
			for i in range(index,work_matrix.shape[0]):
				newBorders = []
				currentSum=sum(work_matrix[i,borderList[j]:borderList[j+1]])
				if currentSum == 0 or  currentSum == (borderList[j+1]-borderList[j]):
					pass
				else:	
					newBorders.append(borderList[j+1]-currentSum)

				current=evaluator(sorted(borderList[j:j+2]+newBorders),borderList[j+1]-borderList[j])
				if current<minimum:
					minimum=current
					position=i
					
			if position in newPositions:
				pass
			else:
				if len(newPositions+selectedTests)<maxNumberOfTests:
					newPositions.append(position)
				else:
					break
					
		for positionIndex in range(0,len(newPositions)):
			indexTable[(index+positionIndex):newPositions[positionIndex]]=np.roll(indexTable[(index+positionIndex):newPositions[positionIndex]],1,0)
			work_matrix[(index+positionIndex):newPositions[positionIndex],:]=np.roll(work_matrix[(index+positionIndex):newPositions[positionIndex],:],1,0)
		
		for j in range(0,len(newPositions)):
			newBorders=[]
	#		print("positions", newPositions)
	#		print(borderList)
			for i in range(len(borderList)-1):
				currentSum=sum(work_matrix[index+j,borderList[i]:borderList[i+1]])
				#print("curr", currentSum)
				if currentSum == 0 or  currentSum == (borderList[i+1]-borderList[i]):
					pass
				else:	
					newBorders.append(borderList[i+1]-currentSum)
	#		print("borders", newBorders)
	#		print(work_matrix)
			for i in range(len(borderList)-1):
				work_matrix[index+j:,borderList[i]: borderList[i+1]]=work_matrix[index+j:, borderList[i]: borderList[i+1]][:,np.argsort(work_matrix[index+j, borderList[i]:borderList[i+1]])]
			borderList = sorted(list(set(borderList + newBorders)))
			work_matrix,borderList=eliminateOnePartitions(borderList,work_matrix)
	#		print(work_matrix)	
		for i in range(len(newPositions)):
			selectedTests.append(indexTable[index+i])
		localizationValue=round(evaluator(borderList,numberOfCols),2)
	#	print(work_matrix)
	print("Fast Fl localizational metric: ", localizationValue)
	#	print("selcted tests: ",selectedTests)
	#	print("borders: ", borderList)
	#print("Runtime: ",time.clock(),"s")
	return localizationValue, selectedTests

"""
Chooses each test randomly, then calculates the localization value.
"""		
def randomSelectionBugLocalizationAlgorithm(input_matrix):
	(numberOfRows,numberOfCols) = input_matrix.shape
	work_matrix = copy.copy(input_matrix)
	localizationValue = 1
	selectedTests = []
	indexTable = np.asarray(list(range(0,input_matrix.shape[0])))
	while len(selectedTests)<maxNumberOfTests and localizationValue>desiredLocalizationValue:# and localizationValue>minimalLocalizationValue:
		index = len(selectedTests)
		position = rnd.randint(index,work_matrix.shape[0])
		indexTable[index:position+1]=np.roll(indexTable[index:position+1],1,0)
		work_matrix[index:position+1,:]=np.roll(work_matrix[index:position+1,:],1,0)
		selectedTests.append(indexTable[index])
	print(selectedTests)	
	exception=np.zeros(numberOfCols)
	tests=0
	for i in range(0,numberOfCols):
		count=0
		if exception[i]==0:
			for j in range(i,numberOfCols):
				if np.array_equal(work_matrix[:len(selectedTests),i],work_matrix[:len(selectedTests),j]) and i!=j:
					count += 1
					exception[j]=1
		tests=tests+count*(count+1)
	expected_value=tests/numberOfCols
	metric=expected_value/(numberOfCols-1)
	print(metric)
	return metric


