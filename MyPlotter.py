'''
Created on 2015.12.15.

@author: Jani
@lector: Zoli
'''

#Imports
from MyUtilities import *


"""
I. ECDF Plotter
"""

"""
Importing necessery variables from "matrix_sums.csv".
"""
matrixNames=[]
matrixSums=[]
labelNames=[]
matrixRows=[]
matrixCols=[]
with open('matrix_sums.csv','r')as csvfile:
	csvReader=csv.reader(csvfile, delimiter=',')
	next(csvReader,None)
	for row in csvReader:
		if row:
			labelNames.append(row[0])
			matrixRows.append(row[1])
			matrixCols.append(row[2])
			del row[0]
			del row[1]
			del row[2]
			matrixSums.append(row)
while (([] in matrixSums)==True):
	matrixSums.remove([])
#print(labelNames)
for i in range(0,14):
	matrixNames.append(labelNames[i]+'.csv')
	matrixRows[i]=int(matrixRows[i])
	matrixCols[i]=int(matrixCols[i])
	for j in range(len(matrixSums[i])):
		matrixSums[i][j]=int(matrixSums[i][j])
#print(matrixSums)
colorList=['b','g','r','y','c','k','m']*3
styleList=['-','--','-.',':']*4
currentNames=[]
currentRows=[]
currentCols=[]

"""
Defining plotter to print ECDF-s to each Cov. Mtx.
"""
def ecdfPlotter(sumsOfMatrices,numberOfRowsInMatrices,normalizationValue,serialNumbersOfMatrices):
	for i in serialNumbersOfMatrices:
		currentNames.append(labelNames[i])
		currentRows.append(matrixRows[i])
		currentCols.append(matrixCols[i])
	print("Starting plotting for matrices at positions:",serialNumbersOfMatrices,"....")
	print("\nNames of Matrices:",currentNames)	
	print("Number of rows in matrices:",currentRows,"\nNumber of columns in matrices:",currentCols)
	if normalizationValue==0:
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			plt.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	elif normalizationValue==1:	
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			xValues=xValues/numberOfRowsInMatrices[i]
			plt.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	elif normalizationValue==2:	
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			yValues=yValues/max(yValues)
			plt.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	else:
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			yValues=yValues/max(yValues)
			xValues=xValues/numberOfRowsInMatrices[i]
			plt.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	plt.legend(loc='lower right')#upper #lower
	plt.xlabel('Number of tests')#distribution #number
	plt.ylabel('Number of procedures')#distribution #number
	plt.grid()
	print("\nSuccesful plotting!")
	plt.show()
	
def ecdfPlotter_GUI(sumsOfMatrices,numberOfRowsInMatrices,normalizationValue,serialNumbersOfMatrices, subplot):
	for i in serialNumbersOfMatrices:
		currentNames.append(labelNames[i])
		currentRows.append(matrixRows[i])
		currentCols.append(matrixCols[i])
	print("Starting plotting for matrices at positions:",serialNumbersOfMatrices,"....")
	print("\nNames of Matrices:",currentNames)	
	print("Number of rows in matrices:",currentRows,"\nNumber of columns in matrices:",currentCols)
	if normalizationValue==0:
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			subplot.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	elif normalizationValue==1:	
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			xValues=xValues/numberOfRowsInMatrices[i]
			subplot.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	elif normalizationValue==2:	
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			yValues=yValues/max(yValues)
			subplot.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	else:
		for i in serialNumbersOfMatrices:
			yValues=[]
			for j in range(0,max(sumsOfMatrices[i])):
				yValues.append(list(sumsOfMatrices[i]).count(j))
			yValues=np.asarray(yValues)
			for j in range(1,len(yValues)):
				yValues[j]=yValues[j]+yValues[j-1]
			xValues=list(np.arange(max(sumsOfMatrices[i])))
			xValues=np.asarray(xValues)
			yValues=yValues-yValues[0]
			yValues=yValues/max(yValues)
			xValues=xValues/numberOfRowsInMatrices[i]
			subplot.plot(xValues,yValues,colorList[i],label=labelNames[i],linewidth=3.0)#linestyle=styleList[i],
	subplot.legend(loc='lower right')#upper #lower
	subplot.set_xlabel('Number of tests')#distribution #number
	subplot.set_ylabel('Number of procedures')#distribution #number
	subplot.grid()
	print("\nSuccesful plotting!")


"""
II. Histogram Plotter
"""
def histPlotter(data,binSize,binSizeType):
	if binSizeType=="Auto":
		plt.hist(data, bins=0, facecolor='g', alpha=1)
	else:
		plt.hist(data,binSize, normed=0, facecolor='g', alpha=1)
	plt.yscale('log', nonposy='clip')
	plt.grid()
	plt.xlabel('Number of tests')
	plt.ylabel('Ratio of procedures')
	print("\nSuccesful plotting!")
	plt.show()