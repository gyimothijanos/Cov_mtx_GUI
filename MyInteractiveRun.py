'''
Created on 2016.01.12.

@author: Jani
@lector: Zoli
'''

from MyBuglocalizationAlgorithm import *
from MyPlotter import *
from MyRarityAlgorithms import *
from MyClassicalAlgorithms import *
from MyHelp import *


"""
Main Menu
"""
def mainMenu():	
	print("\n\nMain menu")
	print("\n1.Importing Matrix")
	print("2.Plotting")
	print("3.Algorithms")
	print("4.Help")
	print("5.Exit")

"""
Importing Menu
"""
def importMenu():
	print("\n\nMatrix Importing Function")
	
	locationList=["C:\munka\Cov_Mtx_Benchmark\Originals\oryx.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\oryx.clover.csv","C:\munka\Cov_Mtx_Benchmark\Originals\orientdb.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\orientdb.clover.csv","C:\munka\Cov_Mtx_Benchmark\Originals\mapdb.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\mapdb.clover.csv","C:\munka\Cov_Mtx_Benchmark\Originals\joda-time.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\joda-time.clover.csv","C:\munka\Cov_Mtx_Benchmark\Originals\commons-math.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\commons-math.clover.csv","C:\munka\Cov_Mtx_Benchmark\Originals\commons-lang.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\commons-lang.clover.csv","C:\munka\Cov_Mtx_Benchmark\Originals\checkstyle.jacoco.csv","C:\munka\Cov_Mtx_Benchmark\Originals\checkstyle.clover.csv"]	
	print("\n")
	print("0.Set new location to import from")
	for i in range(0,14):
		print(str(i+1) + "." + str(locationList[i]))
	print("\n")
	print("\n\n15.Back\n")
	seclectedSerial=int(input("Set location to import from: "))
	if seclectedSerial == 0:
	
		import_matrix_location=input("\nEnter location:\n")
		print("Importing matrix from location: \n" + import_matrix_location + "...")
		df=pd.read_csv(import_matrix_location, sep=",", header=None)
		rawMatrix=df.values
		print("Shape of matrix: ")
		input_matrix=getConvertedMatrix(rawMatrix)
		print("Matrix sucessfully imported!")
		importSucess=1
		return input_matrix
	elif seclectedSerial <= 14 and seclectedSerial >= 1:
	
		import_matrix_location=locationList[seclectedSerial-1]
		print("Importing matrix from location: \n" + import_matrix_location + "...")
		df=pd.read_csv(import_matrix_location, sep=",", header=None)
		rawMatrix=df.values
		print("Shape of matrix: ")
		input_matrix=getConvertedMatrix(rawMatrix)
		print("Matrix sucessfully imported!")
		importSucess=1
		return input_matrix
	elif seclectedSerial == 15:
		import_matrix=0
		mainMenu()

	else:
		print("\nError: Invalid input")
		import_matrix=0
		mainMenu()



"""
Plotting Menu
"""	
def plottingMenu(input_matrix):
	print("\n\nPlotting Function")
	print("\n1.Histogram")
	print("2.Graph")
	print("\n3.Back")
	submenu = int(input("\nChoose a function: "))
	if submenu == 1:
		if type(input_matrix)==int:
			print("Error: No matrix imported")
		else:
			histogramMenu(input_matrix)
	elif submenu ==2:
		graphMenu(input_matrix)
	elif submenu ==3:
		mainMenu()
	else:	
		print("Error: Invalid input")
	return

def histogramMenu(input_matrix):
	print("\n\nHistogram Plotting")
	print("\nDatatypes to select from:")
	print("1.ProcSum")
	print("2.TestSum")
	print("\n3.Back")
	dataType=input("\nSelect a datatype for plotting:")
	if dataType == "3":
		plottingMenu(input_matrix)
	elif dataType == "1":
		data=sum(input_matrix)
		binSizeType=input("Select binsize Type:(Auto/Manual):\n")
		if binSizeType == "Manual":
			binSize=int(input("Set a value for the number of bins:\n"))
		else:
			binSize=0
		histPlotter(data,binSize,binSizeType)
	elif dataType == "2":
		data=sum(input_matrix.T)
		binSizeType=input("Select binsize Type:(Auto/Manual):\n")
		if binSizeType == "Manual":
			binSize=int(input("Set a value for the number of bins:\n"))
		else:
			binSize=0
		histPlotter(data,binSize,binSizeType)
	else:
		print("Error: Invalid input")
	return

def graphMenu(input_matrix):
	serialNumbersOfMatrices=[]
	print("\n\nGraph Plotting")
	print("\nList of matrices")
	print("\n1.oryx.jacoco" + "\n2.oryx.clover" + "\n3.orientdb.jacoco" + "\n4.orientdb.clover" + "\n5.mapdb.jacoco" + "\n6.mapdb.clover" + "\n7.joda-time.jacoco" + "\n8.joda-time.clover" + "\n9.commons-math.jacoco" + "\n10.commons-math.clover" + "\n11.commons-lang.jacoco" + "\n12.commons-lang.clover" + "\n13.checlstyle.jacoco" + "\n14.checlstyle.clover")
	print("\n15.Back")
	listOfSerials=int(input("\nChoose matrix to plot from: "))
	serialNumbersOfMatrices.append(listOfSerials)
	if listOfSerials == 15:
		plottingMenu(input_matrix)
	elif listOfSerials >= 1 and listOfSerials<=14:	
		addSerial = input("\n Do you want to add more matrix for plotting?(y/n) ")
		print("\nList of matrices")
		while addSerial == "y":
			print("\n1.oryx.jacoco" + "\n2.oryx.clover" + "\n3.orientdb.jacoco" + "\n4.orientdb.clover" + "\n5.mapdb.jacoco" + "\n6.mapdb.clover" + "\n7.joda-time.jacoco" + "\n8.joda-time.clover" + "\n9.commons-math.jacoco" + "\n10.commons-math.clover" + "\n11.commons-lang.jacoco" + "\n12.commons-lang.clover" + "\n13.checlstyle.jacoco" + "\n14.checlstyle.clover")
			listOfSerials=int(input("\nChoose matrix to plot from: "))
			if listOfSerials in serialNumbersOfMatrices :
				pass
			else:
				serialNumbersOfMatrices.append(listOfSerials)
			print("Selected serial numbers" + str(serialNumbersOfMatrices))
			addSerial = input("\n Do you want to add a matrix for plotting?(y/n) ")
		removeSerial = input("\n Do you want to remove a matrix from the list?(y/n) ")
		while removeSerial == "y":
			print("\n1.oryx.jacoco" + "\n2.oryx.clover" + "\n3.orientdb.jacoco" + "\n4.orientdb.clover" + "\n5.mapdb.jacoco" + "\n6.mapdb.clover" + "\n7.joda-time.jacoco" + "\n8.joda-time.clover" + "\n9.commons-math.jacoco" + "\n10.commons-math.clover" + "\n11.commons-lang.jacoco" + "\n12.commons-lang.clover" + "\n13.checlstyle.jacoco" + "\n14.checlstyle.clover")
			print("Selected serial numbers" + str(serialNumbersOfMatrices))
			listOfSerials=int(input("\nChoose matrix to remove: "))
			serialNumbersOfMatrices.remove(listOfSerials)
			print("Selected serial numbers" + str(serialNumbersOfMatrices))
			removeSerial = input("\n Do you want to remove a matrix from the list?(y/n) ")
		serialNumbersOfMatrices[:] = [x - 1 for x in serialNumbersOfMatrices]
		print("\nSetting normalization value" + "\n0.No norming" + "\n1.Norming for x axis" + "\n2.Norming for y axis" + "\n3.Norming for both x and y axises")
		normValue=int(input("\nChoose a normalization value: "))
		ecdfPlotter(matrixSums,matrixRows,normValue,serialNumbersOfMatrices)
	else: 
		print("\nError: Invalid input")
	return

"""
Algorithms Menu
"""	
def algorithmMenu(input_matrix):
	print("\n\nCoverage Matrix Analyzing Algorithms")
	print("\n1.Test selection algorithms")
	print("2.Bug localization algorithms")
	print("\n3.Back")
	submenu = int(input("\nChoose a function: "))
	if submenu == 1:
		testSelectionMenu(input_matrix)
	elif submenu ==2:
		bugLocalizationMenu(input_matrix)
	elif submenu ==3:
		mainMenu()
	else:	
		print("Error: Invalid input")
	return

def testSelectionMenu(input_matrix):
	print("\n\nTest Selection Algorithms")
	print("\n1.Classical algorithm")
	print("2.Rarity algorithm")
	print("\n3.Back")
	submenu = int(input("\nChoose a function: "))
	if submenu == 1:
		classicalMenu(input_matrix)
	elif submenu ==2:
		rarityMenu(input_matrix)
	elif submenu ==3:
		algorithmMenu(input_matrix)
	else:
		print("Error: Invalid input")
	return

def classicalMenu(input_matrix):
	print("\n\nClassical Algorithms")
	print("\n1.Classical algorithm")
	print("2.Classical algorithm with prealgoritmic optimalization")
	print("\n3.Back")
	submenu = int(input("\nChoose a function: "))
	if submenu == 1:
		print("\n1.Searching for number of tests chosen to achive the desired coverage")
		print("2.Searching for the coverage rate achived by the given number of maximal chosen test")
		goal=int(input("\nChoose the goal of the algorithm: "))-1
		if goal ==0:
			maximumNumberOfTests=2000
			coverageToAchieve=int(input("\nSet coverage rate to achive: "))
			classicAlg(input_matrix, maximumNumberOfTests, coverageToAchieve)
		elif goal ==1:
			maximumNumberOfTests=int(input("\nSet maximum nuber of selected tests: "))
			coverageToAchieve=100
			classicAlg(input_matrix, maximumNumberOfTests, coverageToAchieve)
		else:
			print("Error: Invalid input")			
	elif submenu ==2:
		print("\n1.Searching for number of tests chosen to achive the desired coverage")
		print("2.Searching for the coverage rate achived by the given number of maximal chosen test")
		goal=int(input("\nChoose the goal of the algorithm: "))-1
		if goal ==0:
			maximumNumberOfTests=2000
			coverageToAchieve=int(input("\nSet coverage rate to achive: "))
			classicalAlgWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve)
		elif goal ==1:
			maximumNumberOfTests=int(input("\nSet maximum nuber of selected tests: "))
			coverageToAchieve=100
			classicalAlgWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve)
		else:
			print("Error: Invalid input")
	elif submenu ==3:
		testSelectionMenu(input_matrix)
	else:
		print("Error: Invalid input")
	return

def rarityMenu(input_matrix):	
	print("\n\nRarity Algorithms")
	print("\n1.Raw rarity algorithm")
	print("2.Weighted rarity algorithm")
	print("3.Raw rarity algorithm with prealgoritmic optimalization")
	print("4.Weighted rarity algorithm with prealgoritmic optimalization")
	print("\n5.Back")
	submenu = int(input("\nChoose a function: "))
	if submenu == 1:
		weight=1
		print("\n1.Searching for number of tests chosen to achive the desired coverage")
		print("2.Searching for the coverage rate achived by the given number of maximal chosen test")
		goal=int(input("\nChoose the goal of the algorithm: "))-1
		if goal ==0:
			maximumNumberOfTests=2000
			coverageToAchieve=int(input("\nSet coverage rate to achive: "))
			rarityAlgorithm(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		elif goal ==1:
			maximumNumberOfTests=int(input("\nSet maximum nuber of selected tests: "))
			coverageToAchieve=100	
			rarityAlgorithm(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		else:
			print("Error: Invalid input")
	elif submenu ==2:
		weight=0
		print("\n1.Searching for number of tests chosen to achive the desired coverage")
		print("2.Searching for the coverage rate achived by the given number of maximal chosen test")
		goal=int(input("\nChoose the goal of the algorithm: "))-1
		if goal ==0:
			maximumNumberOfTests=2000
			coverageToAchieve=int(input("\nSet coverage rate to achive: "))
			rarityAlgorithm(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		elif goal ==1:
			maximumNumberOfTests=int(input("\nSet maximum nuber of selected tests: "))
			coverageToAchieve=100	
			rarityAlgorithm(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		else:
			print("Error: Invalid input")
	elif submenu ==3:
		weight=1
		print("\n1.Searching for number of tests chosen to achive the desired coverage")
		print("2.Searching for the coverage rate achived by the given number of maximal chosen test")
		goal=int(input("\nChoose the goal of the algorithm: "))-1
		if goal ==0:
			maximumNumberOfTests=2000
			coverageToAchieve=int(input("\nSet coverage rate to achive: "))
			rarityAlgorithmWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		elif goal ==1:
			maximumNumberOfTests=int(input("\nSet maximum nuber of selected tests: "))
			coverageToAchieve=100	
			rarityAlgorithmWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		else:
			print("Error: Invalid input")
	elif submenu == 4:
		weight=0
		print("\n1.Searching for number of tests chosen to achive the desired coverage")
		print("2.Searching for the coverage rate achived by the given number of maximal chosen test")
		goal=int(input("\nChoose the goal of the algorithm: "))-1
		if goal ==0:
			maximumNumberOfTests=2000
			coverageToAchieve=int(input("\nSet coverage rate to achive: "))
			rarityAlgorithmWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		elif goal ==1:
			maximumNumberOfTests=int(input("\nSet maximum nuber of selected tests: "))
			coverageToAchieve=100	
			rarityAlgorithmWithOptimalization(input_matrix, maximumNumberOfTests, coverageToAchieve, weight)
		else:
			print("Error: Invalid input")

	elif submenu ==5:
		testSelectionMenu(input_matrix)
	else:
		print("Error: Invalid input")
	return

def bugLocalizationMenu(input_matrix):
	print("\n\nBug Localization Algorithms")
	print("\n There are no such algorithms yet.")
	algorithmMenu(input_matrix)

"""
Help Menu
"""

def helpMenu():
	print("\n1.Help")
	print("2.Documentation")
	print("3.FAQ")
	print("\n\n4.Back")
	submenu = int(input("\nChoose a function: "))	
	if submenu == 1:
		help()
	elif submenu == 2: 
		documentation()
	elif submenu == 3:
		FAQ()
	elif submenu == 4:
		mainMenu()
	else:
		print("Error: Invalid input")

"""
Engine
"""

def interactiveRunner():
	input_matrix=0
	submenu=0
	while submenu!=5:
		mainMenu()
		submenu = int(input("\nChoose a function: "))
		if submenu == 1:
			input_matrix=importMenu()	
		elif submenu == 2:
			plottingMenu(input_matrix)
		elif submenu == 3:
			algorithmMenu(input_matrix)
		elif submenu == 4:
			helpMenu()
		elif submenu != 5:
			print("Error: Invalid input")

#interactiveRunner()