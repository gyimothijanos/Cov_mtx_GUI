"""
Created on 2016.02.01.

@author: Jani
"""

from MyUtilities import *


"""
Calculates the evaluation metric for a given list of partitions.
"""
def getEvaluationMetric(partitionList,numberOfCols):
	evaluationMetric = 0
	for i in partitionList:
		evaluationMetric += (i*(i-1))/(numberOfCols*(numberOfCols-1))
	#print(evaluationMetric)
	return evaluationMetric

"""
Computes the metrical optimum of the matrix
"""
def getMinimalMetric(input_matrix):
	work_matrix = copy.copy(input_matrix)
	borderList = [0,input_matrix.shape[1]]
	for i in range(0,input_matrix.shape[0]):
		newBorders = []
		for j in range(len(borderList)-1):
			currentSum=sum(work_matrix[i,borderList[j]:borderList[j+1]])
			if currentSum == 0 or  currentSum == (borderList[j+1]-borderList[j]):
				pass
			else:	
				newBorders.append(borderList[j+1]-currentSum)
		for k in range(len(borderList)-1):
			work_matrix[ i:,borderList[k]: borderList[k+1]]=work_matrix[ i:, borderList[k]: borderList[k+1]][:,np.argsort(work_matrix[i, borderList[k]:borderList[k+1]])]
		borderList=sorted(borderList+newBorders)
	minimalMetric=evaluator(borderList,input_matrix.shape[1])
	print(minimalMetric)
	return minimalMetric
	
"""
Converted from Matlab code 
"""
def minimalMetricCalculator(input_matrix):
	print(time.clock())
	columns = input_matrix.shape[1]
	exception=np.zeros(columns);
	tests=0;
	for i in range(0,columns):
		count=0
		if exception[i]==0:
			for j in range(i,columns):
				if np.array_equal(input_matrix[:,i],input_matrix[:,j]) and i!=j:
					count += 1
					exception[j]=1
		tests=tests+count*(count+1)
	expected_value=tests/columns
	metric=expected_value/(columns-1)
	print(metric)
	return metric

"""
Calculates the localization metric for a given borderList.
"""
def evaluator(borderVector,numberOfCols):
	partitionList = []
	evaluationMetric = 0
	for i in range(0,len(borderVector)-1):
		partitionList.append(borderVector[i+1]-borderVector[i])
	partitionList = [x for x in partitionList if x != 1]
	for j in range(0,len(partitionList)):
		evaluationMetric += (partitionList[j]*(partitionList[j]-1))/((numberOfCols)*(numberOfCols-1))
	return evaluationMetric

"""
Eliminates the columns which are unique(the size of their partitions is 1) from the matrix.
"""
def eliminateOnePartitions(borderList,work_matrix):
	borderVector = np.asarray(borderList)
	partitionSizes = borderVector[1:]-borderVector[0:-1]
	index = np.nonzero(partitionSizes == 1)
	toRemove = []
	for i in(index):
		toRemove.append(borderVector[i+1]-1)
	#print("Columns to remove: ",toRemove)
	work_matrix = np.delete(work_matrix,toRemove,1)
	counter = np.zeros(len(partitionSizes))
	for k in range(0,len(partitionSizes)):
		if partitionSizes[k] == 1:
			counter[k:] = counter[k:]+1
	#print("Counter list: " , counter)
	borderVector[1:]=borderVector[1:]-counter
	borderList = borderVector.tolist()
	borderList = sorted(list(set(borderList)))
	return work_matrix,borderList

"""
Executes the evaluation of a given Test list.
"""
def evaluateSelectedTests(selectedTestsList,numberOfCols):
	counterDictionary = {selectedTestsList[0]:1}
	partitionList = []
	for i in range(1,len(selectedTestsList)):
		if selectedTestsList[i] in counterDictionary:
			counterDictionary[selectedTestsList[i]] += 1
		else:
			counterDictionary[selectedTestsList[i]] = 1
			
	#print("Partition list:\n", counterDictionary)
	for j in counterDictionary.keys():
		partitionList.append(counterDictionary[j])
	#print("Cardinality of partitions:\n",partitionList)
	evaluationValue = getEvaluationMetric(partitionList,numberOfCols)
	#print("Evaluation Value: ", evaluationValue)
	return evaluationValue 


def evaluateFinalSelectedTests(selectedTestsList,numberOfCols):
	counterDictionary = {selectedTestsList[0]:1}
	partitionList = []
	for i in range(1,len(selectedTestsList)):
		if selectedTestsList[i] in counterDictionary:
			counterDictionary[selectedTestsList[i]] += 1
		else:
			counterDictionary[selectedTestsList[i]] = 1
	print("Partition list:\n", counterDictionary)
	for j in counterDictionary.keys():
		partitionList.append(counterDictionary[j])
	print("Cardinality of partitions:\n",partitionList)
	evaluationValue = getEvaluationMetric(partitionList,numberOfCols)
	return evaluationValue 	

	
"""
Calculates the Fl metric for a given set of tests.
"""
def metricForChosenTests(input_matrix,selectedTests):
	partitions=[]
	(numberOfRows,numberOfCols) = input_matrix.shape
	indexTable = np.asarray(list(range(0,input_matrix.shape[0])))
	work_matrix = copy.copy(input_matrix)
	index = 0	
	for position in(selectedTests):
		x=(indexTable.tolist()).index(position)
		#print("index",x)
		indexTable[index:x+1]=np.roll(indexTable[index:x+1],1,0)
		work_matrix[index:x+1,:]=np.roll(work_matrix[index:x+1,:],1,0)
		index += 1 

	exception=np.zeros(numberOfCols)
	tests=0
	for i in range(0,numberOfCols):
		count=0
		if exception[i]==0:
			for j in range(i,numberOfCols):
				if np.array_equal(work_matrix[:len(selectedTests),i],work_matrix[:len(selectedTests),j]) and i!=j:
					count += 1
					exception[j]=1
			partitions.append(count+1)
		tests=tests+count*(count+1)
	expected_value=tests/numberOfCols
	metric=expected_value/(numberOfCols-1)
	return round(metric,3)
	
