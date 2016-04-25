"""
Created on 2016.02.09.

@author: Jani
"""

from MyBuglocalizationUtilities import *

input_matrix = np.array([[1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0],[1,0,0,0,0,1,0,1,1,0,1,1,0,1,0,0],[0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,0],[0,1,0,1,1,0,1,1,0,1,0,0,1,0,1,1],[0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,0,1,0,0,1,1,0,1,0,0,1,0,1,1]])
desiredLocalizationValue = 0
maxNumberOfTests = 3


def buglocalg(input_matrix):
	numberOfCols = input_matrix.shape[1]
	work_matrix=copy.copy(input_matrix)
	borderList = [0,numberOfCols]
	selectedTestsList = []
	localizationValue = 1
	testSum = sum(input_matrix.T)
	while len(selectedTestsList)<maxNumberOfTests and localizationValue>desiredLocalizationValue:
		if selectedTestsList == []:
			for i in range(0,input_matrix.shape[0]):
				index = 0
				min = numberOfCols
				current=(abs(testSum[i]-numberOfCols/2))
				if current<min:
					min=current
					position=index
				index += index
			
			selectedTestsList.append(position)
			borderList.append(numberOfCols-testSum[position])
			partitionList = [borderList[1],numberOfCols-borderList[1]]
			borderList.sort()
			
		else:
			temporaryBorderList = copy.copy(borderList)
			temporaryBorderList[-1] = temporaryBorderList[-1]-2
			for i in range(len(selectedTestsList),input_matrix.shape[0]):
				index = 1
				min = getEvaluationMetric(partitionList,numberOfCols)
				partitionList = []
				for j in range(0,len(temporaryBorderList)-1):
					partitionList.append(sum(work_matrix[i, temporaryBorderList[j]:temporaryBorderList[j+1]]))
					partitionList.append(temporaryBorderList[j+1]-sum(work_matrix[i, temporaryBorderList[j]:temporaryBorderList[j+1]]))
					current = getEvaluationMetric(partitionList,temporaryBorderList[j+1]-temporaryBorderList[j])
					if current < min:
						min=current
						position=index
				index += index
			selectedTestsList.append(position)

			
			
	print(selectedTestsList,borderList,partitionList)	

					

					
#buglocalg(input_matrix)				



def bugLocalizationAlgorithm2(input_matrix):
	print(input_matrix)
	numberOfCols = input_matrix.shape[1]
	work_matrix=copy.copy(input_matrix)
	borderList = [0,numberOfCols]
	selectedTestsList = []
	localizationValue = 1
	testSum = sum(input_matrix.T)
	serialList = list(range(0,len(testSum)))
	serialList = np.asarray(serialList)
	while len(selectedTestsList)<maxNumberOfTests and localizationValue>desiredLocalizationValue:
		min = 1
		index = len(selectedTestsList)
		partitionList = []
		for i in range(len(selectedTestsList),input_matrix.shape[0]):
			if len(borderList) == 2:
				partitionList.append(numberOfCols-sum(work_matrix[i,:]))
				partitionList.append(sum(work_matrix[i,:]))
				current=getEvaluationMetric(partitionList,numberOfCols)
				if current<min:
					min = current
					position = index
					temporaryBorderList=partitionList
				partitionList = []
				index += index 
			else:
				for j in range(0,len(borderList)-1):
						partitionList.append(borderList[j+1]-borderList[j]-sum(work_matrix[i,borderList[j]:borderList[j+1]]))
						partitionList.append(sum(work_matrix[i,borderList[j]:borderList[j+1]]))	
				current=getEvaluationMetric(partitionList,numberOfCols)
				if current<min:
					min = current
					position = index
					temporaryBorderList=copy.copy(partitionList)
					#print(temporaryBorderList)
				partitionList = []
				index += index 
		serialList[len(selectedTestsList):position+1]=np.roll(serialList[len(selectedTestsList):position+1],1)
		work_matrix[len(selectedTestsList):position+1,:]=np.roll(work_matrix[len(selectedTestsList):position+1,:],1,0)
		selectedTestsList.append(position)
		if temporaryBorderList[0] in borderList:
			pass
		else:
			borderList.append(temporaryBorderList[0])
		permanentPartitionList = copy.copy(temporaryBorderList)
		if (len(temporaryBorderList)%2) == 0:	
			for k in range(2,len(temporaryBorderList),2):
				temporaryBorderList[k] = temporaryBorderList[k]+temporaryBorderList[k-1]+temporaryBorderList[k-2]
				if temporaryBorderList[k] in borderList:	
					pass
				else:
					borderList.append(temporaryBorderList[k])
		
		else:
			for k in range(2,len(temporaryBorderList)-1,2):
				temporaryBorderList[k] = temporaryBorderList[k]+temporaryBorderList[k-1]+temporaryBorderList[k-2]
				if temporaryBorderList[k] in borderList:	
					pass
				else:
					borderList.append(temporaryBorderList[k])
		borderList = sorted(borderList)

	permanentPartitionList= [x for x in permanentPartitionList if x != 0]
	print("Selected tests at positions:",serialList[0:len(selectedTestsList)].tolist(),"\nLocalization value:",getEvaluationMetric(permanentPartitionList,numberOfCols),"\nList of borders: ",borderList,"\nSize of partitions:",permanentPartitionList)				
					
			
bugLocalizationAlgorithm2(input_matrix)
			
			
			