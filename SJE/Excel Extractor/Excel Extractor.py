#! python3
#########################################################################################
# Excel Extractor.py                                                                    #
# Written by Kanyon Edvall                                                              #
#                                                                                       #
# This program allows the user to traverse any spreadsheet and find data of interest    #
# Runs windowless with a GUI made in tkinter                                            #
#########################################################################################


#************************************ Program Setup ************************************#
# Import Everything
import sys, os, re, openpyxl, getpass, base64, base64ico
import tkinter.messagebox
from tkinter import *
from tkinter import ttk, filedialog
from openpyxl.cell import get_column_letter, column_index_from_string


# Global Variables
offset=''
permsFound = []
permsToSearch = []


# Set up GUI
root = Tk() # Create blank window
root.title('Excel Extractor') # Set the name
style = ttk.Style() # Set the style


# Create icon from base64 code
#Base64IconGen(root)


# Class declaration
class FileSelection:
# File Selection Frame (Upper left)

	def __init__(self):
		### Frame setup ###
		fileFrame = ttk.LabelFrame(root, text='File Selection: ', padding='3 3 12 12') # Make a themed frame to hold objects
		fileFrame.grid(columnspan=6, row=0, pady=10, sticky='N W S E')

		# Required variables
		FileSelection.filePath = StringVar()
		self.selectedSheet = StringVar()
		self.fileDisp = StringVar()

		# File opening options
		self.fileOpt = options = {}
		options['defaultextension'] = '.xlsx'
		options['filetypes'] = [('Excel', '.xlsx'), ('Spreadsheet', '.xlsm'), ('Spreadsheet', '.xltx'), ('Spreadsheet', '.xltm')]
		options['initialdir'] = 'C:\\Users\\' + getpass.getuser() + '\\Documents'
		options['parent'] = fileFrame
		options['title'] = 'Select a File to Use'

		# Interface elements
		self.fileBtn = ttk.Button(fileFrame, text='Select File:', style='fileBtn.TButton', command=self.askDir)
		root.bind('<Return>', self.eventPass)
		self.fileBtn.focus_set()
		self.fileBtn.grid(columnspan=3, row=1, sticky=E)
		self.fileEntry = ttk.Entry(fileFrame, width=50, textvariable=self.filePath)
		self.fileEntry.grid(columnspan=3, column=4, row=1, sticky=W)

		ttk.Label(fileFrame, text='Select Sheet:').grid(columnspan=3, row=2, sticky=E)
		self.sheetCBox = ttk.Combobox(fileFrame, textvariable=self.selectedSheet, width=30, state='readonly')
		self.sheetCBox['values'] = ''
		self.sheetCBox.grid(columnspan=3, column=4, row=2, sticky=W)

		self.loadBtn = ttk.Button(fileFrame, text='Load File', style='loadBtn.TButton')
		self.loadBtn.state(['disabled'])
		self.loadBtn.grid(columnspan=3, row=3, sticky='W S')
		ttk.Label(fileFrame, textvariable=self.fileDisp).grid(columnspan=3, column=4, row=3, sticky='W S')

		for child in fileFrame.winfo_children(): child.grid_configure(padx=5, pady=10)


	def eventPass(self, event):
		self.askDir()


	def askDir(self):
		# Open ask directory dialog and set path
		self.filename = filedialog.askopenfilename(**self.fileOpt)
		if self.filename:
			FileSelection.filePath.set(self.filename)
			root.bind('<Return>', self.loadFile)
			self.loadBtn.bind('<Button-1>', self.loadFile)
			self.loadBtn.state(['!disabled'])
			self.loadBtn.focus_set()
			self.loadWorkbook()
		style.configure('fileBtn.TButton', relief=RAISED)


	def loadWorkbook(self):
	# Load workbook and setup sheet selection
		try:
			FileSelection.wb = openpyxl.load_workbook(FileSelection.filePath.get())
			self.sheetCBox['values'] = FileSelection.wb.get_sheet_names()
			self.sheetCBox.current(self.sheetCBox['values'].index(FileSelection.wb.active.title))
		except FileNotFoundError:
			self.fileDisp.set('Could not load file at ' + self.filename)


	def loadFile(self, event):
		# Load selected sheet from workbook
		try:
			FileSelection.sheet = FileSelection.wb.get_sheet_by_name(self.selectedSheet.get())
			self.fileDisp.set('Successfully loaded ' + str(self.selectedSheet.get()) + '.')
			ParamSelection.paramFrame.grid()
			Search.searchFrame.grid()
		except KeyError:
			self.fileDisp.set('Error loading ' + str(self.selectedSheet.get()) + '!')
		

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
	

class ParamSelection:
# Parameter selection frame (Upper right)
	def __init__(self):
		### Frame setup ###
		ParamSelection.paramFrame = ttk.LabelFrame(root, text='Search Options: ', padding='3 3 12 12')
		ParamSelection.paramFrame.grid(columnspan=6, pady=10, row=3, sticky='N W S E')

		# Required variables
		ParamSelection.searchCol = StringVar() # Holds name of column to be searched
		ParamSelection.pasteCol = StringVar() # Holds name of column to paste data into
		ParamSelection.offsetMode = StringVar() # Currently select offset mode (Radio button)
		ParamSelection.offsetPattern = StringVar() # Holds text from pattern entry field
		ParamSelection.vcmd = ParamSelection.paramFrame.register(self.updateHandler) # Validation binding
		self.offsetPtrnLbl = StringVar() # Holds text of label above pattern entry
		ParamSelection.curDraw = 'pattern'

		# Set defaults
		ParamSelection.searchCol.set('Column: A to XFD')
		ParamSelection.pasteCol.set('Column: A to XFD')
		ParamSelection.offsetMode.set('pattern')

		# Interface elements
		ttk.Label(ParamSelection.paramFrame, text='Which column would you like to search?').grid(columnspan=5, row=0, sticky=E)
		self.sColEntry = ttk.Entry(ParamSelection.paramFrame, width=17, textvariable=ParamSelection.searchCol, foreground='grey', validate='all', validatecommand=(self.vcmd, '%V', '%W', '%P'))
		self.sColEntry.grid(columnspan=2, column=5, row=0, sticky=W)
		
		ttk.Label(ParamSelection.paramFrame, text='Which column would you like to copy the selected data to?').grid(columnspan=5, row=1, sticky=E)
		self.pColEntry = ttk.Entry(ParamSelection.paramFrame, width=17, textvariable=ParamSelection.pasteCol, foreground='grey', validate='all', validatecommand=(self.vcmd, '%V', '%W', '%P'))
		self.pColEntry.grid(columnspan=2, column=5, row=1, sticky=W)

		ttk.Label(ParamSelection.paramFrame, text='').grid(columnspan=7, row=2, sticky=(W, E)) # Divider
		ttk.Label(ParamSelection.paramFrame, text='Select Offset Type:').grid(columnspan=3, row=3, sticky=W)
		ttk.Label(ParamSelection.paramFrame, text='Pattern Configuration:').grid(columnspan=5, column=2, row=3, sticky=W)

		self.patternRBtn = ttk.Radiobutton(ParamSelection.paramFrame, text='Pattern', variable=ParamSelection.offsetMode, value='pattern', command=self.radioSet)
		self.patternRBtn.grid(column=0, row=4, sticky=W)
		self.charRBtn = ttk.Radiobutton(ParamSelection.paramFrame, text='Character Count', variable=ParamSelection.offsetMode, value='char', command=self.radioSet)
		self.charRBtn.grid(column=1, row=4, sticky=W)
		self.configBtn = ttk.Button(ParamSelection.paramFrame, text='Set Up Search Pattern', style='configBtn.TButton', command=self.clickConfigure)
		self.configBtn.grid(columnspan=5, column=2, row=4, sticky=W)
		
		ParamSelection.nameDict = {str(self.sColEntry):{'textvar':ParamSelection.searchCol, 'placeholder':'Column: A to XFD', 'entryName':self.sColEntry, 'type':'column'},
						 str(self.pColEntry):{'textvar':ParamSelection.pasteCol, 'placeholder':'Column: A to XFD', 'entryName':self.pColEntry, 'type':'column'}}

		for child in ParamSelection.paramFrame.winfo_children(): child.grid_configure(padx=5, pady=5)
		ParamSelection.paramFrame.grid_remove()


	def radioSet(self):
		try:
			if ParamSelection.offsetMode.get() == 'pattern':
				self.updateHandler('radioChange', 'radioTriggerMapping', ParamSelection.offsetPattern.get())
			else:
				self.updateHandler('radioChange', 'radioTriggerMapping', ParamSelection.offsetPattern.get())
		except KeyError:
			return


	def updateHandler(self, reason, varName, entryValue): 
	# Called on entry state change, decides where to pass task. Return True to allow edit, False to disallow
		if reason == 'radioChange' and ParamSelection.curDraw == 'char': # Radio button was clicked, check new position
			if (not self.validateEntry(varName, entryValue) or ParamSelection.offsetPattern.get() == ''):
				self.setPlaceholder(varName, True)

		elif reason == 'focusin':
			self.remPlaceholder(varName)

		elif reason == 'focusout':
			self.setPlaceholder(varName, False)

		elif reason == 'key':
			if not self.validateEntry(varName, entryValue):
				return False

			elif ParamSelection.nameDict[varName]['type'] == 'pattern':
				if entryValue != '':
					self.toggleEnable('en')
				else:
					self.toggleEnable('dis')
		return True		


	def validateEntry(self, varName, curEntryVal):
	# Validates the entry based on entry type. Returns True if pass, False if fail
		if ParamSelection.nameDict[varName]['type'] == 'column':
			if not (curEntryVal.isalpha() or curEntryVal == ''):
				return False
			elif curEntryVal != '':
				try:
					column_index_from_string(str(curEntryVal).upper())
				except ValueError:
					return False

		elif ParamSelection.offsetMode.get() == 'char':
			if not (curEntryVal.isdigit() or curEntryVal == ''):
				return False

		return True


	def setPlaceholder(self, varName, forceSet):
	# Sets the placeholder text of the entry. Can be forced to override current text
		textvar = ParamSelection.nameDict[varName]['textvar']

		if forceSet: # If force flag is set, override current value
			textvar.set(ParamSelection.nameDict[varName]['placeholder'])
			ParamSelection.nameDict[varName][str('entryName')].configure(foreground='grey')

		elif textvar.get() == '': # Check if Entry is empty before setting value
			if (ParamSelection.nameDict[varName]['type'] == 'pattern' and ParamSelection.offsetMode.get() == 'char'): # If pattern entry, make sure char is selected
				textvar.set(ParamSelection.nameDict[varName]['placeholder'])
				ParamSelection.nameDict[varName][str('entryName')].configure(foreground='grey')

			elif ParamSelection.nameDict[varName]['type'] == 'column': # Column entry
				textvar.set(ParamSelection.nameDict[varName]['placeholder'])
				ParamSelection.nameDict[varName][str('entryName')].configure(foreground='grey')


	def remPlaceholder(self, varName):
	# Removes the placeholder text of the entry
		textvar = ParamSelection.nameDict[varName]['textvar']

		if textvar.get() == ParamSelection.nameDict[varName]['placeholder']:
			textvar.set('')
			ParamSelection.nameDict[varName][str('entryName')].configure(foreground='black')


	def toggleEnable(self, state):
		if state == 'en':
			Search.termEntry.configure(state='enabled')
			Search.searchOptionsBtn.configure(state='enabled')
			Search.permutBtn.configure(state='enabled')
		else:
			Search.termEntry.configure(state='disabled')
			Search.searchOptionsBtn.configure(state='disabled')
			Search.permutBtn.configure(state='disabled')


	def clickConfigure(self):
		PatternDialog()


class PatternDialog():
	def __init__(self):
		# Close any previous toplevel instance (clicking button more than once)
		try:
			PatternDialog.toplevel.destroy()
		except AttributeError:
			pass

		# Create and center the toplevel window
		PatternDialog.toplevel = Toplevel()
		PatternDialog.toplevel.title('Pattern Search Configuration')
		self.topFrame = Frame(PatternDialog.toplevel)
		self.bottomFrame = Frame(PatternDialog.toplevel)
		self.topFrame.pack(fill=X, expand=True)
		self.bottomFrame.pack(side=BOTTOM, fill=X, expand=True)

		# Variables
		PatternDialog.rulesDict = {}

		# Create icon from base64 code
		Base64IconGen(PatternDialog.toplevel)

		# Get screen dimensions
		self.rX = root.winfo_rootx()
		self.rY = root.winfo_rooty()
		self.rHeight = root.winfo_height()
		self.rWidth = root.winfo_width()

		# Pass drawing frame depending on offset mode
		if ParamSelection.offsetMode.get() == 'char':
			self.drawChar()
			ParamSelection.curDraw = 'char'
		else:
			self.drawPattern()
			ParamSelection.curDraw = 'pattern'

		
	def drawChar(self):
		ttk.Label(self.topFrame, text='Enter number of characters:').pack(side=TOP, anchor=W)

		self.ptrnEntry = ttk.Entry(self.topFrame, width=30, textvariable=ParamSelection.offsetPattern, validate='all', validatecommand=(ParamSelection.vcmd, '%V', '%W', '%P'))
		self.ptrnEntry.pack(side=TOP, anchor=W, padx=2, pady=5)
		ParamSelection.nameDict[str(self.ptrnEntry)] = {'textvar':ParamSelection.offsetPattern, 'placeholder':'Must be a number (Ex 10)', 'entryName':self.ptrnEntry, 'type':'pattern'}
		ParamSelection.nameDict['radioTriggerMapping'] = {'textvar':ParamSelection.offsetPattern, 'placeholder':'Must be a number (Ex 10)', 'entryName':self.ptrnEntry, 'type':'pattern'}
		ParamSelection.setPlaceholder(ParamSelection, str(self.ptrnEntry), False)
	
		self.drawButtons()


	def drawPattern(self):
		ttk.Label(self.topFrame, text='Match the following rules:').pack(side=TOP, anchor=W)

		self.drawButtons()


	def drawButtons(self):
		cancelBtn = ttk.Button(self.bottomFrame, text='Cancel', command=self.cancelDialog, style='cancelBtn.TButton')
		cancelBtn.pack(side=LEFT)
		doneBtn = ttk.Button(self.bottomFrame, text='Done', command=self.doneDialog, style='doneBtn.TButton')
		doneBtn.pack(side=RIGHT)

		for child in PatternDialog.toplevel.winfo_children(): child.pack_configure(padx=5, pady=5)

		root.update_idletasks()
		size = list(int(item) for item in PatternDialog.toplevel.geometry().split('+')[0].split('x'))
		if size[0] < 325:
			size[0] = 325
		geometry = "%dx%d+%d+%d" % (size[0], size[1], self.rX + ((self.rWidth / 2) - (size[0] / 2)), self.rY + ((self.rHeight / 2) - (size[1] / 2)))
		PatternDialog.toplevel.geometry(geometry)


	def cancelDialog(self):
		ParamSelection.offsetPattern.set('')
		PatternDialog.toplevel.destroy()


	def doneDialog(self):
		PatternDialog.toplevel.destroy()


class Search:
# Search Frame (Lower right)
	def __init__(self):
		### Outer Frame setup ###
		Search.searchFrame = ttk.LabelFrame(root, text='Search: ', padding='3 3')
		Search.searchFrame.grid(columnspan=6, column=7, rowspan=4, row=0, pady=10, sticky='N W S E')

		# Required variables
		self.searchTerm = StringVar()
		self.selectStateText = StringVar()
		self.selectStateText.set('Select All')
		self.cbVals={}
		self.resultCB={}
		self.lbl={}
		
		# Interface elements
		ttk.Label(Search.searchFrame, text='Enter search term:').grid(columnspan=2, row=2, sticky='W')
		Search.termEntry = ttk.Entry(Search.searchFrame, width=53, textvariable=self.searchTerm)
		Search.termEntry.bind('<FocusIn>', self.createHandler)
		Search.termEntry.grid(columnspan=5, column=2, row=2, sticky=W)
		Search.termEntry.configure(state='disabled')
		
		Search.searchOptionsBtn = ttk.Button(Search.searchFrame, text='Search Options', command=self.optionsDialog, style='searchOptionsBtn.TButton')
		Search.searchOptionsBtn.grid(column=0, row=3, sticky='W')
		self.instructionLbl = ttk.Label(Search.searchFrame, text="A period will allow any non alphanumeric character to be substituted in it's place.", wraplength=350)
		self.instructionLbl.grid(columnspan=6, column=1, row=3, sticky='W')
		Search.searchOptionsBtn.configure(state='disabled')

		specialLbl = ttk.Label(Search.searchFrame, text='Available Permutations:').grid(columnspan=3, row=4, sticky='W S')
		Search.permutBtn = ttk.Button(Search.searchFrame, text='Search Permutations', command=self.searchPerms, style='permutBtn.TButton')
		Search.permutBtn.grid(columnspan=2, column=5, row=4, sticky=E)
		Search.permutBtn.configure(state='disabled')

		Search.startSearchBtn = ttk.Button(Search.searchFrame, text='Start Search', command=self.startSearch, style='startSearchBtn.TButton')
		Search.startSearchBtn.grid(row=9, sticky=W)
		Search.selectBtn = ttk.Button(Search.searchFrame, textvariable=self.selectStateText, command=self.switchState, style='selectBtn.TButton')
		Search.selectBtn.grid(columnspan=5, column=1, row=9)
		Search.exportBtn = ttk.Button(Search.searchFrame, text='Export Sheet', command=self.exportSheet, style='exportBtn.TButton')
		Search.exportBtn.grid(columnspan=2, column=6, row=9, sticky=E)
		Search.startSearchBtn.configure(state='disabled')
		Search.selectBtn.configure(state='disabled')
		Search.exportBtn.configure(state='disabled')

		for child in Search.searchFrame.winfo_children(): child.grid_configure(padx=5, pady=10)
		Search.searchOptionsBtn.grid_configure(pady=0)
		self.instructionLbl.grid_configure(padx=7, pady=0)

		### Inner Frame Setup ###
		self.resultFrameTop = ttk.Frame(Search.searchFrame, borderwidth=0, relief='groove', padding='3 3 170 120')
		self.resultFrameTop.grid(columnspan=7, row=5, padx=5, sticky='N W S E')
		self.resultFrameBot = ttk.Frame(Search.searchFrame, borderwidth=0)
		self.resultFrameBot.grid(columnspan=7, rowspan=2, row=6, padx=5, sticky='N W S E')

		# Required Variables
		self.results = StringVar()
		self.results.set('Waiting for search term...')
		Search.drawCalled = False

		# Interface elements
		ttk.Label(self.resultFrameTop, textvariable=self.results).pack(side=LEFT)
		Search.searchFrame.grid_remove()


	def createHandler(self, event):
		ExcelHandler(FileSelection, ParamSelection)

	
	def drawResults(self):
		# Setup result headings
		self.results.set('')
		self.resultFrameTop.configure(relief='flat', padding='0 0 0 0')
		self.resultFrameTop.grid_configure(padx=1)
		self.resultHLbl = ttk.Label(self.resultFrameTop, text='Result:' + ' ' * 25)
		self.resultHLbl.pack(side=LEFT)
		self.posHLbl = ttk.Label(self.resultFrameTop, text='Row/Col:' + ' ' * 10)
		self.posHLbl.pack(side=LEFT)
		self.contextHLbl = ttk.Label(self.resultFrameTop, text='Context:')
		self.contextHLbl.pack(side=LEFT)

		# Set up frame
		self.scrollbar = Scrollbar(self.resultFrameBot, orient=VERTICAL)
		self.resultbox = Listbox(self.resultFrameBot, selectmode=MULTIPLE, yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.resultbox.yview)
		self.scrollbar.pack(side=RIGHT, fill=Y, padx=0, pady=0)
		self.resultbox.pack(fill=BOTH, expand=1, padx=0, pady=0)

		# Remove all items from previous list
		self.resultbox.delete(1, END)
		# Set called var
		Search.drawCalled = True


	def optionsDialog(self):
		print('Options!')


	def searchPerms(self):
	# Search the selected spreadsheet for the specified permutations and generate any requested ones
		# Check if the user actually entered something
		if self.searchTerm.get() != '':
			# Enable buttons
			Search.startSearchBtn.configure(state='enabled')
			Search.selectBtn.configure(state='enabled')
			Search.exportBtn.configure(state='enabled')

			# Draw result box if it's not already there
			if not Search.drawCalled:
				self.drawResults()
			
			# Remove all items from previous list
			self.resultbox.delete(0, END)

			# Generate permutations based on search terms
			RegexGeneration.genPerms(RegexGeneration, str(self.searchTerm.get()))
			ExcelHandler.findPerms(ExcelHandler)
			
			# Print results
			for item in permsFound:
				if not (item in self.resultbox.get(0, "end")):
					self.resultbox.insert(END, item)
		else:
			tkinter.messagebox.showinfo('Error', 'Please enter a term to search for.')


	def switchState(self):
		if self.selectStateText.get() == 'Deselect All':
			self.selectStateText.set('Select All')
			self.resultbox.selection_clear(0, END)
		else:
			self.selectStateText.set('Deselect All')
			self.resultbox.selection_set(0, END)


	def startSearch(self):
		self.translateSelection()
		ExcelHandler.searchSheet(ExcelHandler)
		tkinter.messagebox.showinfo('Progress', 'Finished Search.')


	def translateSelection(self):
		# Correlates the currently selected listbox items to their string values using the permsFound list
		global permsToSearch
		permsToSearch = self.resultbox.curselection()
		permsToSearch = [permsFound[int(item)] for item in permsToSearch]


	def exportSheet(self):
		exportPath = os.path.dirname(ExcelHandler.filePath) + os.sep + 'extracted_' + os.path.basename(ExcelHandler.filePath)
		ExcelHandler.wb.save(exportPath)
		text = 'Exported to ' + exportPath
		tkinter.messagebox.showinfo('Export', text)


class ExcelHandler(FileSelection, ParamSelection):
# Class to handle traversing Excel sheets
	def __init__(self, files, params):
		RegexGeneration.parseOffset(RegexGeneration)
		ExcelHandler.filePath = files.filePath.get()
		ExcelHandler.wb = files.wb
		ExcelHandler.sheet = files.sheet
		ExcelHandler.searchCol = column_index_from_string(str(params.searchCol.get()).upper())
		ExcelHandler.pasteCol = column_index_from_string(str(params.pasteCol.get()).upper())
		

	def findPerms(self):
		global permsFound
		for rowNum in range (1, ExcelHandler.sheet.max_row + 1):
			curCell = ExcelHandler.sheet.cell(row=rowNum, column=ExcelHandler.searchCol)
			for result in RegexGeneration.permutRegex.findall(str(curCell.value)):
				if result[0] not in (' '.join(permsFound)):
					permsFound.append(result[0])


	def getPermInfo(self):
		print('Placeholder for getting Row/Col and Context info')


	def searchSheet(self):
		for term in permsToSearch:
			for rowNum in range (1, ExcelHandler.sheet.max_row + 1):
				curCell = ExcelHandler.sheet.cell(row=rowNum, column=ExcelHandler.searchCol)
				startIndex = str(curCell.value).find(term)
				if startIndex != -1:
					print('Found match for ' + term + ' at ' + str(curCell)) #Eventually change to live feedback popup (scrolls with this text)
					self.matchItem(self, curCell, ExcelHandler.sheet.cell(row=rowNum, column=ExcelHandler.pasteCol))


	def matchItem(self, searchCell, pasteCell):
		try:
			result = RegexGeneration.patternRegex.search(searchCell.value)
			if result != None:
				pasteCell.value = result.group()
		except TypeError:
			return


class RegexGeneration:
# Class to handle all regular expression and pattern generation
	def genPerms(self, originTerm):
	# Generate permutations to search for based on search term
		if '.' not in originTerm:
			searchStrings = originTerm.split()
			searchStrings = '([\\-_ /])*'.join(searchStrings)
			RegexGeneration.permutRegex = re.compile(r'(' + searchStrings + ')+', re.I)

		else:
			searchStrings = originTerm.split()
			searchStrings = '([\\-_ /])*'.join(searchStrings)
			searchStrings = originTerm.split('.')
			searchStrings = '([\\-_ /])*'.join(searchStrings)
			RegexGeneration.permutRegex = re.compile(r'(' + searchStrings + ')+', re.I)


	def parseOffset(self):
		pattern = ParamSelection.offsetPattern.get()
		RegexGeneration.patternRegex = re.compile(r'(' + pattern + ')', re.I)


	def searchPtrn(self):
		print('Pattern')


class Base64IconGen():
# Takes icon from base64 format and creates window icon
	def __init__(self, window):
		icondata = base64.b64decode(base64ico.extractorIcon)
		# The temp file is icon.ico
		tempFile= "icon.ico"
		iconfile= open(tempFile,"wb")
		# Extract the icon
		iconfile.write(icondata)
		iconfile.close()
		window.wm_iconbitmap(tempFile)
		# Delete the tempfile
		os.remove(tempFile)


#************************************ Program Start ************************************#
# Create objects
Base64IconGen(root)
filePane = FileSelection()
sModePane = SearchSelection()
paramPane = ParamSelection()
searchPane = Search()

# Run GUI
root.mainloop()