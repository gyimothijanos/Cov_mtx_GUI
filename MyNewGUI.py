"""
Tkinter GUI for the Coverage Matrix Analyzing program
"""

import os, fnmatch
from tkinter import *
from MyInteractiveRun import *
from matplotlib import pyplot as plt
from MyUtilities import *
from MyBuglocalizationUtilities import *
from MyBuglocalizationAlgorithm import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

LARGE_FONT = ("Helvetica", 14)
MEDIUM_FONT = ("Helvetica", 11)
SMALL_FONT = ("Helvetica", 8)

class covMatrixAnalyzingApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		self.container = tk.Frame(self)
		self.container.pack(side = "top", fill = "both", expand = True)
		self.container.grid_rowconfigure(0, weight = 1)
		self.container.grid_columnconfigure(0, weight = 1)
		
		tk.Tk.wm_title(self, "Coverage Matrix Analyzation")
		tk.Tk.iconbitmap(self,default='icon.ico')
		self.frames = {}

		self.input_matrix, self.directoryInUse, self.matrixName =self.importMatrix()
		print(self.input_matrix)
		
		self.generateBasicInformationCSV()
		
		for F in (mainMenu, plottingMenu, algorithmMenu, helpMenu, histogramMenu, graphMenu, testSelectionMenu, bugLocalizationMenu):

			frame = F(self.container, self, self.input_matrix)

			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky = "nsew")

		self.show_frame(mainMenu)

	def show_frame(self, cont):
		if cont == histogramMenu or graphMenu or testSelectionMenu or bugLocalizationMenu:
			for F in (histogramMenu,graphMenu, testSelectionMenu, bugLocalizationMenu):
				
				frame = F(self.container, self, self.input_matrix)
				self.frames[F] = frame
				frame.grid(row = 0, column = 0, sticky = "nsew")
		frame = self.frames[cont]
		frame.tkraise()
		
	def importMatrix(self):
		fileName=tk.filedialog.askopenfilename(title="Select a matrix to import")
		print("Importing matrix from location: \n" + fileName + "...")
		df=pd.read_csv(fileName, sep=",", header=None)
		raw_matrix=df.values
		self.input_matrix=getConvertedMatrix(raw_matrix)
		print("Shape of matrix: ")
		separatedFileNameList = fileName.split("/",)
		self.matrixName = separatedFileNameList[-1].replace(".csv","")
		separatedFileNameList.remove(separatedFileNameList[-1])
		self.directoryInUse = "/".join(separatedFileNameList) + "/"
		print(self.matrixName)
		print("Matrix sucessfully imported!")
		return self.input_matrix, self.directoryInUse, self.matrixName
	
	def findCSV(self, pattern, path):
		result = []
		for root, dirs, files in os.walk(path):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
					result.append(os.path.join(root, name))
		if result == []:
			print("no such file found")
			return result
		else:
			print(result[0])
			return result[0]
	
	def generateBasicInformationCSV(self):
		os.chdir(self.directoryInUse)
		if self.findCSV(self.matrixName + '_general_information.csv', os.getcwd()) == []:
			covValue = round(maximalCoverageCalculator(self.input_matrix),2)
			flMetric = round(getMinimalMetric(self.input_matrix),3)
			d = []
			d.append(round(flMetric,3))
			d.insert(0,covValue)
			d.insert(0,self.input_matrix.shape[1])
			d.insert(0,self.input_matrix.shape[0])
			d.insert(0,self.matrixName)
			print(d)
			with open(self.matrixName + '_general_information.csv', 'w', newline='') as f:
				w = csv.writer(f)
				w.writerow(['Matrix name','Number of rows','Number of columns','Maximal coverage value (%)','Minimal "FL"Metrics'])
				w.writerow(d)
		else:
			pass
		if self.findCSV(self.matrixName + '_simulation_results.csv', os.getcwd()) != []:
			pass
		else:
			b = open(self.matrixName + '_simulation_results.csv', 'w')
			a = csv.writer(b,delimiter=',',quoting=csv.QUOTE_ALL)
			a.writerow(["Type of optimalization", "Real coverage value (%)", "Fl metric value", "Number of selected tests", "Selected test positions (starting from 0)"])
			b.close()
		
class mainMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Main menu", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		plotButton = ttk.Button(self, text="Plotting", width=30, command = lambda: controller.show_frame(plottingMenu))
		plotButton.pack(padx=25, pady=25)
		algorithmButton = ttk.Button(self, text="Algorithms", width=30, command = lambda: controller.show_frame(algorithmMenu))
		algorithmButton.pack(padx=25, pady=25)
		helpButton = ttk.Button(self, text="Help", width=30, command = lambda: controller.show_frame(helpMenu))
		helpButton.pack(padx=25, pady=25)
		
		exitButton = ttk.Button(self, text="Exit", width=30, command = self.quit)
		exitButton.pack(padx=25, pady=25)

class plottingMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Plotting menu", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		histButton = ttk.Button(self, text="Histogram", width=30, command = lambda: controller.show_frame(histogramMenu))
		histButton.pack(padx=25, pady=25)
		graphButton = ttk.Button(self, text="Graph", width=30, command = lambda: controller.show_frame(graphMenu))
		graphButton.pack(padx=25, pady=25)
		
		backButton = ttk.Button(self, text="Back", command = lambda: controller.show_frame(mainMenu))
		backButton.pack(padx=25, pady=25, side=LEFT)
				
class algorithmMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Algorithm menu", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		testSelButton = ttk.Button(self, text = "Coverage maximizing algorithms", command = lambda: controller.show_frame(testSelectionMenu))
		testSelButton.pack(padx = 25, pady = 25)
		
		bugLocButton = ttk.Button(self, text = "Bug localizational algorithms", command = lambda:controller.show_frame(bugLocalizationMenu))
		bugLocButton.pack(padx = 25, pady = 25)
		
		backButton = ttk.Button(self, text="Back", command = lambda: controller.show_frame(mainMenu))
		backButton.pack(padx=25, pady=25, side=LEFT)

class helpMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Help", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		backButton = ttk.Button(self, text="Back", command = lambda: controller.show_frame(mainMenu))
		backButton.pack(padx=25, pady=25, side=LEFT)
		
class histogramMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Histogram plotting", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		self.var1 = tk.IntVar()
		procSumChoose = tk.Checkbutton(self, text="ProcSum", variable = self.var1, onvalue=1, offvalue = 0, command = lambda: self.procSum(input_matrix))
		procSumChoose.pack(padx=25)

		self.var2 = tk.IntVar()
		testSumChoose = tk.Checkbutton(self, text="TestSum", variable = self.var2, onvalue=1, offvalue = 0, command = lambda: self.testSum(input_matrix)) 
		testSumChoose.pack(padx=25)
		
		self.var3 = tk.IntVar()
		autoBinSize =tk.Checkbutton(self, text="Automatical Binsize", variable = self.var3, onvalue=1, offvalue = 0, command = lambda: self.autoBin())
		autoBinSize.pack(padx=25)
		
		self.var4 = tk.IntVar()
		manualBinSize = tk.Checkbutton(self, text="Manual Binsize", variable = self.var4, onvalue=1, offvalue = 0, command = lambda: self.manualBin())
		manualBinSize.pack(padx=25)
		
		plotButton = ttk.Button(self, text="Plot histogram", command = lambda: self.plotHist(input_matrix))
		plotButton.pack()
		
		backButton = ttk.Button(self, text="Back", command = lambda: controller.show_frame(plottingMenu))
		backButton.pack(padx=25, pady=25, side=LEFT)
	
	def autoBin(self):
		if self.var3.get() == 1:
			self.binSizeType = "Auto"
			print(self.binSizeType)
			return self.binSizeType
	def manualBin(self):
		if self.var4.get() == 1:
			
			self.binSize=tk.IntVar()
			binSizeScale = tk.Scale(self, from_=0, to=500, orient=tk.HORIZONTAL, tickinterval=100, length = 300, takefocus = True, sliderlength = 20, variable = self.binSize)
			binSizeScale.pack()
			
			self.binSizeType = "Manual"
			print(self.binSizeType)
			return self.binSize, self.binSizeType
			
	def procSum(self,input_matrix):
		if self.var1.get() == 1:
			self.data = sum(input_matrix)
			print("procSum", self.data)
			return self.data
	def testSum(self,input_matrix):
		if self.var2.get() == 1:
			self.data = sum(input_matrix.T)
			print("testSum", self.data)
			return self.data
			
	def plotHist(self,input_matrix):
		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_subplot(111)
		if self.binSizeType == "Auto":	
			a.hist(self.data, bins=range(int(min(self.data)), int(max(self.data)) + int(1), int(1)), facecolor='g', alpha=1)
			if len(self.data) == len(sum(input_matrix)): 
				a.set_xlabel('Number of tests')
				a.set_ylabel('Ratio of procedures')
			else:
				a.set_xlabel('Number of procedures')
				a.set_ylabel('Ratio of tests')
			a.grid()
			a.set_yscale('log', nonposy='clip')
		else:
			a.hist(self.data, self.binSize.get(), normed=0, facecolor='g', alpha=1)
			if (len(self.data) == len(sum(input_matrix))): 
				a.set_xlabel('Number of tests')
				a.set_ylabel('Ratio of procedures')
			else:
				a.set_xlabel('Number of procedures')
				a.set_ylabel('Ratio of tests')
			a.grid()
			a.set_yscale('log', nonposy='clip')
		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		toolbar = NavigationToolbar2TkAgg(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		
class graphMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Graph plotting", font = LARGE_FONT)
		label.pack(padx=25, pady=25)

		plotButton = ttk.Button(self, text="Plot histogram", command = lambda: self.plotGraph())
		plotButton.pack(side = BOTTOM)

		backButton = ttk.Button(self, text="Back", command = lambda: controller.show_frame(plottingMenu))
		backButton.pack(side = LEFT, anchor = "sw")
	
		self.var1 = IntVar()
		self.var2 = IntVar()
		self.var3 = IntVar()
		self.var4 = IntVar()
		self.var5 = IntVar()
		self.var6 = IntVar()
		self.var7 = IntVar()
		self.var8 = IntVar()
		self.var9 = IntVar()
		self.var10 = IntVar()
		self.var11 = IntVar()
		self.var12 = IntVar()
		self.var13 = IntVar()
		self.var14 = IntVar()
		self.serialNumbersOfMatrices = []
		mtx1 = tk.Checkbutton(self, text="1.oryx.jacoco", variable = self.var1, onvalue=20, offvalue = 0, command = lambda: self.selectSerial(0))
		mtx1.pack(side=TOP, anchor = "w")
		mtx2 = tk.Checkbutton(self, text="2.oryx.clover", variable = self.var2, onvalue=1, offvalue = 0, command = lambda: self.selectSerial(1))
		mtx2.pack(side=TOP, anchor = "w")
		mtx3 = tk.Checkbutton(self, text="3.orientdb.jacoco", variable = self.var3, onvalue=2, offvalue = 0, command = lambda: self.selectSerial(2))
		mtx3.pack(side=TOP, anchor = "w")
		mtx4 = tk.Checkbutton(self, text="4.orientdb.clover", variable = self.var4, onvalue=3, offvalue = 0, command = lambda: self.selectSerial(3))
		mtx4.pack(side=TOP, anchor = "w")
		mtx5 = tk.Checkbutton(self, text="5.mapdb.jacoco", variable = self.var5, onvalue=4, offvalue = 0, command = lambda: self.selectSerial(4))
		mtx5.pack(side=TOP, anchor = "w")
		mtx6 = tk.Checkbutton(self, text="6.mapdb.clover", variable = self.var6, onvalue=5, offvalue = 0, command = lambda: self.selectSerial(5))
		mtx6.pack(side=TOP, anchor = "w")
		mtx7 = tk.Checkbutton(self, text="7.joda-time.jacoco", variable = self.var7, onvalue=6, offvalue = 0, command = lambda: self.selectSerial(6))
		mtx7.pack(side=TOP, anchor = "w")
		mtx8 = tk.Checkbutton(self, text="8.joda-time.clover", variable = self.var8, onvalue=7, offvalue = 0, command = lambda: self.selectSerial(7))
		mtx8.pack(side=TOP, anchor = "w")
		mtx9 = tk.Checkbutton(self, text="9.commons-math.jacoco", variable = self.var9, onvalue=8, offvalue = 0, command = lambda: self.selectSerial(8))
		mtx9.pack(side=TOP, anchor = "w")
		mtx10 = tk.Checkbutton(self, text="10.commons-math.clover", variable = self.var10, onvalue=9, offvalue = 0, command = lambda: self.selectSerial(9))
		mtx10.pack(side=TOP, anchor = "w")
		mtx11 = tk.Checkbutton(self, text="11.commons-lang.jacoco", variable = self.var11, onvalue=10, offvalue = 0, command = lambda: self.selectSerial(10))
		mtx11.pack(side=TOP, anchor = "w")
		mtx12 = tk.Checkbutton(self, text="12.commons-lang.clover", variable = self.var12, onvalue=11, offvalue = 0, command = lambda: self.selectSerial(11))
		mtx12.pack(side=TOP, anchor = "w")
		mtx13 = tk.Checkbutton(self, text="13.checlstyle.jacoco", variable = self.var13, onvalue=12, offvalue = 0, command = lambda: self.selectSerial(12))
		mtx13.pack(side=TOP, anchor = "w")
		mtx14 = tk.Checkbutton(self, text="14.checlstyle.clover", variable = self.var14, onvalue=13, offvalue = 0, command = lambda: self.selectSerial(13) )
		mtx14.pack(side=TOP, anchor = "w")
		
		self.normValue = IntVar()
		
		normLabel = tk.Label(self, text="Select normalization")
		normLabel.pack(side = TOP, anchor = "w")
		
		normOption = ttk.Radiobutton(self, text="no normalizing", variable = self.normValue, value = 0)
		normOption2 = ttk.Radiobutton(self, text="x axis normalizing", variable = self.normValue, value = 1)
		normOption3 = ttk.Radiobutton(self, text="y axis normalizing", variable = self.normValue, value = 2)
		normOption4 = ttk.Radiobutton(self, text="x & y axis normalizing", variable = self.normValue, value = 3)
		
		normOption.pack(side = LEFT, anchor = "n")
		normOption2.pack(side = LEFT, anchor = "n")
		normOption3.pack(side = LEFT, anchor = "n")
		normOption4.pack(side = LEFT, anchor = "n")
		
		self.variable_list=[self.var1, self.var2, self.var3, self.var4, self.var5, self.var6, self.var7, self.var8, self.var9, self.var10, self.var11, self.var12, self.var13, self.var14]
		
	def selectSerial(self, serial):
		if self.variable_list[serial] == self.var1:
			if self.variable_list[serial].get() == 20:
				self.serialNumbersOfMatrices.append(serial)
			else:
				self.serialNumbersOfMatrices.remove(serial)
		elif self.variable_list[serial].get() != 0 :
			self.serialNumbersOfMatrices.append(serial)
		else:
			self.serialNumbersOfMatrices.remove(serial)

	def plotGraph(self):
		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_subplot(111)
		ecdfPlotter_GUI(matrixSums,matrixRows,self.normValue.get(),self.serialNumbersOfMatrices, a)
		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		toolbar = NavigationToolbar2TkAgg(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	
class testSelectionMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Coverage maximizing algorithms", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		label = tk.Label(self, text="Select algorithm", font = MEDIUM_FONT)
		label.pack(padx=25, pady=10)
		
		self.algType = tk.IntVar()
		algType = ttk.Radiobutton(self, text="Classical algorithm", variable = self.algType, value = 0)
		algType2 = ttk.Radiobutton(self, text="Raw rariry algorithm", variable = self.algType, value = 1)
		algType3 = ttk.Radiobutton(self, text="Weighted rarity algorithm", variable = self.algType, value = 2)
		algType.pack()
		algType2.pack()
		algType3.pack()
		
		label = tk.Label(self, text="Specify the type of the algorithm", font = MEDIUM_FONT)
		label.pack(padx=25, pady=10)

		self.algOpt = tk.IntVar()
		algOptimalization = ttk.Radiobutton(self, text="Without prealgoritmic optimalization", variable = self.algOpt, value = 0)
		algOptimalization2 = ttk.Radiobutton(self, text="With prealgoritmic optimalization", variable = self.algOpt, value = 1)
		algOptimalization.pack()
		algOptimalization2.pack()
		
		label = tk.Label(self, text="Specify the goal of the algorithm", font = MEDIUM_FONT)
		label.pack(padx=25, pady=10)
		
		self.goalVariable = tk.IntVar()
		setGoal = ttk.Radiobutton(self, text="Searching for number of tests chosen to achive the desired coverage", variable = self.goalVariable, value = 1, command = lambda: self.setCovRate())
		setGoal2 = ttk.Radiobutton(self, text="Searching for the coverage rate achived by the given number of maximal chosen test", variable = self.goalVariable, value = 2, command = lambda: self.setMaxNumOfTests())
		setGoal.pack()
		setGoal2.pack()
		
		startAlg = ttk.Button(self, text = "Start the algorithm", command = lambda: self.specifyCovAlgorithm(input_matrix))
		startAlg.pack()
		
		backButton = ttk.Button(self, text= "Back", command = lambda: controller.show_frame(algorithmMenu))
		backButton.pack(side = LEFT, padx = 25, pady = 25)
	
		self.maximumNumberOfTests = 2000
		self.coverageToAchieve = 100

	def setCovRate(self):
		self.coverageToAchieve = tk.IntVar()
		setCovRateToAchive = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=10, length = 300, sliderlength = 20,  variable = self.coverageToAchieve)
		setCovRateToAchive.pack()
		
	def setMaxNumOfTests(self):
		self.maximumNumberOfTests = tk.IntVar()
		setMaxNumberOfTest = tk.Scale(self, from_=0, to=1500, orient=tk.HORIZONTAL, tickinterval=75, length = 900, sliderlength = 20,  variable = self.maximumNumberOfTests)
		setMaxNumberOfTest.pack()
	
	def findCSV(self, pattern, path):
		result = []
		for root, dirs, files in os.walk(path):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
					result.append(os.path.join(root, name))
		if result == []:
			print("no such file found")
			return result
		else:
			print(result[0])
			return result[0]
	
	def	specifyCovAlgorithm(self, input_matrix):
		a=self.maximumNumberOfTests
		b=self.coverageToAchieve
		goal = self.goalVariable.get()-1
		if goal == 0:
			b = self.coverageToAchieve.get()+1-1
		elif goal == 1:
			a = self.maximumNumberOfTests.get()+1-1
		if self.algType.get() == 0:
			if self.algOpt.get() == 0:
				if goal == 0:
					b = self.coverageToAchieve.get()+1-1
				elif goal == 1:
					a = self.maximumNumberOfTests.get()+1-1
				selectedTestPositions , sumCoverage = classicAlg(input_matrix, a, b)
				optimalizationtype = "Classical coverage alg."
			else:
				if goal == 0:
					b = self.coverageToAchieve.get()+1-1
				elif goal == 1:
					a = self.maximumNumberOfTests.get()+1-1
				selectedTestPositions , sumCoverage = classicalAlgWithOptimalization(input_matrix, a, b)
				optimalizationtype = "Classical coverage alg with prealgopt."
		elif self.algType.get() == 1:
			weight=1
			if self.algOpt.get() == 0:
				if goal == 0:
					b = self.coverageToAchieve.get()+1-1
				elif goal == 1:
					a = self.maximumNumberOfTests.get()+1-1
				selectedTestPositions , sumCoverage = rarityAlgorithm(input_matrix, a, b, weight)
				optimalizationtype = "Raw rarity alg."
			else:
				if goal == 0:
					b = self.coverageToAchieve.get()+1-1
				elif goal == 1:
					a = self.maximumNumberOfTests.get()+1-1
				selectedTestPositions , sumCoverage = rarityAlgorithmWithOptimalization(input_matrix, a, b, weight)
				optimalizationtype = "Raw rarity alg with prealgopt."
		elif self.algType.get() == 2:
			weight=0
			if self.algOpt.get() == 0:
				if goal == 0:
					b = self.coverageToAchieve.get()+1-1
				elif goal == 1:
					a = self.maximumNumberOfTests.get()+1-1	
				selectedTestPositions , sumCoverage = rarityAlgorithm(input_matrix, a, b, weight)
				optimalizationtype = "Weighted rarity alg."
			else:
				if goal == 0:
					b = self.coverageToAchieve.get()+1-1
				elif goal == 1:
					a = self.maximumNumberOfTests.get()+1-1
				selectedTestPositions , sumCoverage = rarityAlgorithmWithOptimalization(input_matrix, a, b, weight)
				optimalizationtype = "Weighted rariry alg with prealgopt."
				
		if True == messagebox.askyesno("Result of the algorithm", ("Number of tests chosen by the algorithm:", len(selectedTestPositions), "\nCoverage percentage achieved by the algorithm:", sumCoverage, "%","\nFl metric achieved by the selected tests:", metricForChosenTests(input_matrix,selectedTestPositions),"\n\nDo you want to save these results?")):
			d = []
			d.append(selectedTestPositions)
			d.insert(0,len(selectedTestPositions))
			d.insert(0,metricForChosenTests(input_matrix,selectedTestPositions))
			d.insert(0,sumCoverage)
			d.insert(0,optimalizationtype)
			print(d)
			
			bla = open(self.findCSV('*results.csv', os.getcwd()), 'a')
			alb = csv.writer(bla,delimiter=',',quoting=csv.QUOTE_ALL)
			alb.writerow(d)
			bla.close()
		else:
			pass


class bugLocalizationMenu(tk.Frame):
	
	def __init__(self, parent, controller, input_matrix):	
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Bug localization algorithms", font = LARGE_FONT)
		label.pack(padx=25, pady=25)
		
		label = tk.Label(self, text="Select algorithm", font = MEDIUM_FONT)
		label.pack(padx=25, pady=10)
	
		self.algType = tk.IntVar()
		algType = ttk.Radiobutton(self, text="Optimal buglocalization algorithm", variable = self.algType, value = 0)
		algType2 = ttk.Radiobutton(self, text="Fast buglocalization algorithm", variable = self.algType, value = 1)
		algType.pack()
		algType2.pack()
		
		label = tk.Label(self, text="Specify the goal of the algorithm", font = MEDIUM_FONT)
		label.pack(padx=25, pady=10)
		
		self.maximumNumberOfTests = 2000
		self.flRateToAchieve = 0
		
		self.goalVariable = tk.DoubleVar()
		setGoal = ttk.Radiobutton(self, text="Searching for number of tests chosen to achive the desired fl value", variable = self.goalVariable, value = 1, command = lambda: self.setFlRate())
		setGoal2 = ttk.Radiobutton(self, text="Searching for the fl metric achived by the given number of maximal chosen test", variable = self.goalVariable, value = 2, command = lambda: self.setMaxNumOfTests())
		setGoal.pack()
		setGoal2.pack()
			
		startAlg = ttk.Button(self, text = "Start the algorithm", command = lambda: self.specifyFlAlgorithm(input_matrix))
		startAlg.pack()
		
		backButton = ttk.Button(self, text= "Back", command = lambda: controller.show_frame(algorithmMenu))
		backButton.pack(side = LEFT, padx = 25, pady = 25)

	
	def setFlRate(self):
		self.flRateToAchieve = tk.DoubleVar()
		setCovRateToAchive = tk.Scale(self, from_=1.0, to=0.0, orient=tk.HORIZONTAL, resolution= 0.01, tickinterval = 0.1, length = 400, sliderlength = 20,  variable = self.flRateToAchieve)
		setCovRateToAchive.pack()
		
	def setMaxNumOfTests(self):
		self.maximumNumberOfTests = tk.IntVar()
		setMaxNumberOfTest = tk.Scale(self, from_=0, to=1500, orient=tk.HORIZONTAL, tickinterval=75, length = 900, sliderlength = 20,  variable = self.maximumNumberOfTests)
		setMaxNumberOfTest.pack()
	
	def findCSV(self, pattern, path):
		result = []
		for root, dirs, files in os.walk(path):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
					result.append(os.path.join(root, name))
		if result == []:
			print("no such file found")
			return result
		else:
			print(result[0])
			return result[0]
	
	def specifyFlAlgorithm(self, input_matrix):	
		a=self.maximumNumberOfTests
		b=self.flRateToAchieve
		goal = self.goalVariable.get()-1
		if goal == 0:
			b = self.flRateToAchieve.get()+1-1
		elif goal == 1:
			a = self.maximumNumberOfTests.get()+1-1
		if self.algType.get() == 0:
			flMetric, selectedTestPositions = optimalBugLocalizationAlgorithm(input_matrix,a , b)
			optimalizationtype = "Optimal buglocalization alg."
		elif self.algType.get() == 1:
			flMetric, selectedTestPositions = fastBugLocalizationAlgorithm(input_matrix, a, b)
			optimalizationtype = "Fast buglocalization alg."
		
		if True == messagebox.askyesno("Result of the algorithm", ("Number of tests chosen by the algorithm:", len(selectedTestPositions), "\nFl metric achieved by the algorithm:", flMetric,"\nCoverage rate achieved by the selected tests:", coverageRateForChosenTests(input_matrix, selectedTestPositions), "%","\n\nDo you want to save these results?")):
			d = []
			d.append(selectedTestPositions)
			d.insert(0,len(selectedTestPositions))
			d.insert(0,flMetric)
			d.insert(0,coverageRateForChosenTests(input_matrix, selectedTestPositions))	
			d.insert(0,optimalizationtype)
			print(d)
			
			bla = open(self.findCSV('*results.csv', os.getcwd()), 'a')
			alb = csv.writer(bla,delimiter=',',quoting=csv.QUOTE_ALL)
			alb.writerow(d)
			bla.close()
		else:
			pass
	
	
app = covMatrixAnalyzingApp()
app.mainloop()