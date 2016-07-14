from tkinter import *
from tkinter import ttk, filedialog
import tkinter.messagebox
import getpass

# Variables
search=''
match=''
offset=''
permutations = []

# Set up GUI
root = Tk() # Create blank window
root.title('Excel Data Scraper') # Set the name
style = ttk.Style()


# Class declaration
class FileSelection:
	# File Selection Frame (Upper left)
	def __init__(self):
		# Frame setup
		fileFrame = ttk.LabelFrame(root, text='File Selection: ', padding='3 3 12 12') # Make a themed frame to hold objects
		fileFrame.grid(columnspan=6, row=0, pady=10, sticky='N W S E')

		# Required variables
		self.filePath = StringVar()
		self.selectedSheet = StringVar()
		self.fileDisp = StringVar()

		# File opening options
		self.fileOpt = options = {}
		options['defaultextension'] = '.xlsx'
		options['filetypes'] = [('Excel', '.xlsx'), ('Spreadsheet', '.xlsm'), ('Spreadsheet', '.xltx'), ('Spreadsheet', '.xltm'), ('All Files', '.*')]
		options['initialdir'] = 'C:\\Users\\' + getpass.getuser() + '\\Documents'
		options['parent'] = fileFrame
		options['title'] = 'Select a File to Use'

		# Interface elements
		self.fileBtn = ttk.Button(fileFrame, text='Select File:', style='fileBtn.TButton')
		self.fileBtn.bind('<Button-1>', self.askDir)
		root.bind('<Return>', self.askDir)
		self.fileBtn.focus_set()
		self.fileBtn.grid(columnspan=3, row=1, sticky=E)
		self.fileEntry = ttk.Entry(fileFrame, width=50, textvariable=self.filePath)
		self.fileEntry.grid(columnspan=3, column=4, row=1, sticky=W)

		ttk.Label(fileFrame, text='Select Sheet:').grid(columnspan=3, row=2, sticky=E)
		self.sheetCBox = ttk.Combobox(fileFrame, textvariable=self.selectedSheet, state='readonly')
		self.sheetCBox.bind('<<ComboboxSelected>>', self.doSomething)
		self.sheetCBox['values'] = ('Sheet1', 'Sheet2', 'Sheet3')
		self.sheetCBox.current(0)
		self.sheetCBox.grid(columnspan=3, column=4, row=2, sticky=W)

		self.loadBtn = ttk.Button(fileFrame, text='Load File', style='loadBtn.TButton')
		self.loadBtn.state(['disabled'])
		self.loadBtn.grid(columnspan=3, row=3, sticky='W S')
		ttk.Label(fileFrame, textvariable=self.fileDisp).grid(columnspan=3, column=4, row=3, sticky='W S')

		for child in fileFrame.winfo_children(): child.grid_configure(padx=5, pady=10)

		#dividerFrame = ttk.Frame(root, padding='3 3 12 12')
		#dividerFrame.grid(columnspan=6, row=1, sticky='N W S E')
		#ttk.Label(dividerFrame, text='').grid(columnspan=6, row=1, sticky='W E') # Divider

	def doSomething(self, event):
		print('Box moved')

	def loadFile(self, event):
		self.fileDisp.set('Successfully loaded: ' + str(self.filePath.get()))
		print('File Loaded!!!')

	def askDir(self, event):
		self.filename = filedialog.askopenfilename(**self.fileOpt)
		if self.filename:
			self.filePath.set(self.filename)
			self.loadBtn.state(['!disabled'])
			self.loadBtn.bind('<Button-1>', self.loadFile)
			self.loadBtn.focus_set()
			root.bind('<Return>', self.loadFile)
		style.configure('fileBtn.TButton', relief=RAISED)
		

class SearchSelection:
	# Search Selection Frame (Lower left)
	def __init__(self):
		# Frame setup
		sModeFrame = ttk.LabelFrame(root, text='Search Type: ', padding='3 3 12 12')
		sModeFrame.grid(columnspan=6, row=2, pady=10, sticky='N S W E')
		
		# Required variables
		self.searchMode = StringVar()
		self.searchMode.set('keyword')
		self.matchMode = StringVar()
		self.matchMode.set('column')
		self.radioSet()

		# Interface elements
		ttk.Label(sModeFrame, text='Select Search Mode:').grid(columnspan=6, row=1, sticky=W)
		self.keywordRBtn = ttk.Radiobutton(sModeFrame, text='Keyword', variable=self.searchMode, value='keyword', command=self.radioSet)
		self.keywordRBtn.grid(columnspan=3, row=2, sticky=W)
		self.exactRBtn = ttk.Radiobutton(sModeFrame, text='Exact Match', variable=self.searchMode, value='exact', command=self.radioSet)
		self.exactRBtn.grid(columnspan=3, column=4, row=2, sticky=W)

		ttk.Label(sModeFrame, text='').grid(column=0, row=3, sticky=(W, E)) # Divider
		ttk.Label(sModeFrame, text='Select Match Mode:').grid(columnspan=6, row=4, sticky=W)
		self.columnRBtn = ttk.Radiobutton(sModeFrame, text='From Another Column', variable=self.matchMode, value='column', command=self.radioSet)
		self.columnRBtn.grid(columnspan=3, row=5, sticky=W)
		self.offsetRBtn = ttk.Radiobutton(sModeFrame, text='Keyword Offset', variable=self.matchMode, value='offset', command=self.radioSet)
		self.offsetRBtn.grid(columnspan=3, column=4, row=5, sticky=W)

		for child in sModeFrame.winfo_children(): child.grid_configure(padx=5, pady=0)
		
	def radioSet(self):
		search = self.searchMode.get()
		match = self.matchMode.get()
		print(search + match)
	

class ParamSelection:
	# Parameter selection frame (Upper right)
	def __init__(self):
		# Frame setup
		paramFrame = ttk.LabelFrame(root, text='Search Options: ', padding='3 3 12 12')
		paramFrame.grid(columnspan=6, column=7, pady=10, row=0, sticky='N W S E')

		# Required variables
		self.searchCol = StringVar()
		self.searchCol.set('Column: A to XFD')
		self.pasteCol = StringVar()
		self.pasteCol.set('Column: A to XFD')
		self.offsetMode = StringVar()
		self.offsetMode.set('pattern')
		self.offsetPtrnLbl = StringVar()
		self.offsetPtrnLbl.set('Enter Pattern:')
		self.offsetPattern = StringVar()

		# Interface elements
		ttk.Label(paramFrame, text='Which column would you like to search?').grid(columnspan=5, row=0, sticky=E)
		self.sColEntry = ttk.Entry(paramFrame, width=17, textvariable=self.searchCol, foreground='grey')
		self.sColEntry.bind('<Button-1>', self.clearEntry)
		self.sColEntry.bind('<FocusOut>', self.resetEntry)
		self.sColEntry.grid(columnspan=2, column=5, row=0, sticky=W)

		ttk.Label(paramFrame, text='Which column would you like to copy the selected data to?').grid(columnspan=5, row=1, sticky=E)
		self.pColEntry = ttk.Entry(paramFrame, width=17, textvariable=self.pasteCol, foreground='grey')
		self.pColEntry.bind('<Button-1>', self.clearEntry)
		self.pColEntry.bind('<FocusOut>', self.resetEntry)
		self.pColEntry.grid(columnspan=2, column=5, row=1, sticky=W)

		ttk.Label(paramFrame, text='').grid(columnspan=7, row=2, sticky=(W, E)) # Divider
		ttk.Label(paramFrame, text='Select Offset Type:').grid(columnspan=3, row=3, sticky=W)
		ttk.Label(paramFrame, textvariable=self.offsetPtrnLbl).grid(columnspan=5, column=2, row=3, sticky=W)

		self.patternRBtn = ttk.Radiobutton(paramFrame, text='Pattern', variable=self.offsetMode, value='pattern', command=self.radioSet)
		self.patternRBtn.grid(column=0, row=4, sticky=W)
		self.charRBtn = ttk.Radiobutton(paramFrame, text='Character Count', variable=self.offsetMode, value='char', command=self.radioSet)
		self.charRBtn.grid(column=1, row=4, sticky=W)
		self.ptrnEntry = ttk.Entry(paramFrame, width=30, textvariable=self.offsetPattern)
		self.ptrnEntry.grid(columnspan=5, column=2, row=4, sticky=W)

		for child in paramFrame.winfo_children(): child.grid_configure(padx=5, pady=5)

	def clearEntry(self, event):
		if event.widget is self.sColEntry:
			if self.searchCol.get() == 'Column: A to XFD':
				self.sColEntry.configure(foreground='black')
				self.searchCol.set('')
		elif event.widget is self.pColEntry:
			if self.pasteCol.get() == 'Column: A to XFD':
				self.pColEntry.configure(foreground='black')
				self.pasteCol.set('')

	def resetEntry(self, event):
		if event.widget is self.sColEntry:
			if self.searchCol.get() == '':
				self.sColEntry.configure(foreground='grey')
				self.searchCol.set('Column: A to XFD')
		if event.widget is self.pColEntry:
			if self.pasteCol.get() == '':
				self.pColEntry.configure(foreground='grey')
				self.pasteCol.set('Column: A to XFD')

	def radioSet(self):
		offset=self.offsetMode.get()
		print(offset)
		if self.offsetMode.get() == 'pattern':
			self.offsetPtrnLbl.set('Enter Pattern:')
		else:
			self.offsetPtrnLbl.set('Enter Offset (Number of characters):')


class Search:
	# Search Frame (Lower right)
	def __init__(self):
		# Outer Frame setup
		searchFrame = ttk.LabelFrame(root, text='Search: ', padding='3 3 12 12')
		searchFrame.grid(columnspan=6, column=7, row=2, pady=10, sticky='N W S E')

		# Required variables
		self.searchTerm = StringVar()
		self.selectState = StringVar()
		self.selectState.set('Unselect All')
		self.cbVals={}
		self.resultCB={}
		self.lbl={}
		
		# Interface elements
		ttk.Label(searchFrame, text='Enter search term:').grid(columnspan=2, row=2, sticky='W')
		self.termEntry = ttk.Entry(searchFrame, width=53, textvariable=self.searchTerm)
		self.termEntry.grid(columnspan=5, column=2, row=2, sticky=W)
		
		ttk.Label(searchFrame, text='Available Permutations:').grid(columnspan=3, row=3, sticky='W S')
		self.permutBtn = ttk.Button(searchFrame, text='Search Permutations', style='permutBtn.TButton')
		self.permutBtn.bind('<Button-1>', self.searchPerms)
		self.permutBtn.grid(columnspan=2, column=5, row=3, sticky=E)

		self.startSearchBtn = ttk.Button(searchFrame, text='Start Search', style='startSearchBtn.TButton')
		self.startSearchBtn.bind('<Button-1>', self.doSomething)
		self.startSearchBtn.grid(columnspan=2, row=7, sticky=W)
		self.selectBtn = ttk.Button(searchFrame, textvariable=self.selectState, style='selectBtn.TButton')
		self.selectBtn.bind('<Button-1>', self.switchState)
		self.selectBtn.grid(columnspan=4, column=2, row=7)
		self.exportBtn = ttk.Button(searchFrame, text='Export Sheet', style='exportBtn.TButton')
		self.exportBtn.bind('<Button-1>', self.doSomething)
		self.exportBtn.grid(columnspan=2, column=5, row=7, sticky=E)

		for child in searchFrame.winfo_children(): child.grid_configure(padx=5, pady=10)

		# Inner Frame Setup
		self.resultFrame = ttk.Frame(searchFrame, borderwidth=5, relief='groove', padding='3 3 120 120')
		self.resultFrame.grid(columnspan=7, rowspan=3, row=4, padx=5, sticky='N W S E')

		# Required Variables
		self.results = StringVar()
		self.results.set('Waiting for search term...')

		# Interface elements
		ttk.Label(self.resultFrame, textvariable=self.results).grid(columnspan=6, rowspan=3)

	def doSomething(self, event):
		print('Btn clicked')

	def searchPerms(self, event):
		# For testing #
		for i in range(0, 7):
			self.lbl[i] = ttk.Label(self.resultFrame, text=[i])
			self.lbl[i].grid(column=[i], row=0, sticky=W)

		for index in range(1, 11):
			permutations.append('Result ' + str(index))

		# Setup result headings
		self.results.set('')
		self.resultFrame.configure(padding='3 3 12 12')

		self.resultHLbl = ttk.Label(self.resultFrame, text='Result: ')
		self.resultHLbl.grid(columnspan=2, row=1, sticky=W)
		self.posHLbl = ttk.Label(self.resultFrame, text='Row/Col: ')
		self.posHLbl.grid(columnspan=2, column=2, row=1, sticky=W)
		self.contextHLbl = ttk.Label(self.resultFrame, text='Context: ')
		self.contextHLbl.grid(columnspan=2, column=4, row=1, sticky=W)
		
		# Enumerate results
		for i in range(len(permutations)):
			print('Iteration ' + str(i))
			self.cbVals[i] = StringVar()
			self.cbVals[i].set(1)
			self.resultCB[i] = ttk.Checkbutton(self.resultFrame, text=permutations[i], variable=self.cbVals[i])
			self.resultCB[i].bind('<Button-1>', self.updatePerms)
			self.resultCB[i].grid(columnspan=2, column=0, row=[i+2], sticky=W)

		for child in self.resultFrame.winfo_children(): child.grid_configure(padx=5)

	def updatePerms(self, event):
		print('Item state changed')

	def switchState(self, event):
		if self.selectState.get() == 'Unselect All':
			for box in self.resultCB:
				self.cbVals[box].set(0)
			self.updatePerms(None)
			self.selectState.set('Select All')
		else:
			for box in self.resultCB:
				self.cbVals[box].set(1)
			self.updatePerms(None)
			self.selectState.set('Unselect All')


filePane = FileSelection()
sModePane = SearchSelection()
paramPane = ParamSelection()
searchPane = Search()

root.mainloop()