#! python3
#########################################################################################
# IFS Importer.py                                                                       #
# Written by Kanyon Edvall                                                              #
#                                                                                       #
# This program allows the user to easily import data into IFS                           #
# More IFS functionality may be added later                                             #
#########################################################################################


#                                                                                       #
# ************************************************************************************* #
# DATA VALIDATION:                                                                      #
#   - Puts data into IFS, then goes through IFS entries (read-only) and check against   #
#     precomputed Excel values                                                          #
#   - No new data is extracted                                                          #
# ************************************************************************************* #
#                                                                                       #


#************************************ Program Setup ************************************#
# Import everything
import sys, os, re, subprocess, getpass, openpyxl, pyautogui, pahk, base64, base64ico
import tkinter.messagebox
from tkinter import *
from tkinter import ttk, filedialog
from openpyxl.cell import get_column_letter, column_index_from_string
from pahk import Interpreter
from time import sleep

# Set Up GUI
root = Tk()
root.title('IFS Importer') # Set the name
style = ttk.Style() # Set the style

# Create icon from base64 code
icondata = base64.b64decode(base64ico.importerIcon)
# The temp file is icon.ico
tempFile= "icon.ico"
iconfile= open(tempFile,"wb")
# Extract the icon
iconfile.write(icondata)
iconfile.close()
root.wm_iconbitmap(tempFile)
# Delete the tempfile
os.remove(tempFile)


############################################################################################################################
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
			ColumnSelection.mainFrame.grid()
		except KeyError:
			self.fileDisp.set('Error loading ' + str(self.selectedSheet.get()) + '!')
		

############################################################################################################################
class ColumnSelection:
# Parameter selection frame (Upper right)

	def __init__(self):
		### Frame setup ###
		ColumnSelection.mainFrame = ttk.LabelFrame(root, text='Import Options: ', padding='3 3 12 12')
		ColumnSelection.mainFrame.grid(columnspan=6, pady=10, row=3, sticky='N W S E')

		# Subframes to hold various elements
		ColumnSelection.titleFrame = ttk.Frame(ColumnSelection.mainFrame)
		ColumnSelection.titleFrame.pack(side=TOP, fill=X, expand=True)
		ColumnSelection.entryFrame = ttk.Frame(ColumnSelection.mainFrame)
		ColumnSelection.entryFrame.pack(fill=X, expand=True)
		ColumnSelection.addBtnFrame = ttk.Frame(ColumnSelection.mainFrame)
		ColumnSelection.addBtnFrame.pack(side=BOTTOM, fill=X, expand=True)

		### Required variables ###
		ColumnSelection.columnsToImportDict = {} # Dictionary for user entered columns

		### Interface elements ###
		ttk.Label(ColumnSelection.titleFrame, text='Select columns to import data from:').pack(anchor=W) # Instruction label

		# Create a add button
		EntryHandler.addButton = ttk.Button(ColumnSelection.addBtnFrame, text='Add Another Import Column', command=EntryHandler.addImport)
		EntryHandler.addButton.pack(anchor=W, pady=5, padx=5)

		ImportColumn() # Add entry field

		# Add spacing to all widgets within this frame
		#for child in ColumnSelection.mainFrame.winfo_children(): child.grid_configure()
		# Temporarily hid this frame
		ColumnSelection.mainFrame.grid_remove()

	'''
	def validateEntry(self, varName, curEntryVal):
	# Validates the entry based on entry type. Returns True if pass, False if fail
		if self.nameDict[varName]['type'] == 'column':
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
		textvar = self.nameDict[varName]['textvar']

		if forceSet: # If force flag is set, override current value
			textvar.set(self.nameDict[varName]['placeholder'])
			self.nameDict[varName][str('entryName')].configure(foreground='grey')

		elif textvar.get() == '': # Check if Entry is empty before setting value
			if (self.nameDict[varName]['type'] == 'pattern' and ParamSelection.offsetMode.get() == 'char'): # If pattern entry, make sure char is selected
				textvar.set(self.nameDict[varName]['placeholder'])
				self.nameDict[varName][str('entryName')].configure(foreground='grey')

			elif self.nameDict[varName]['type'] == 'column': # Column entry
				textvar.set(self.nameDict[varName]['placeholder'])
				self.nameDict[varName][str('entryName')].configure(foreground='grey')


	def remPlaceholder(self, varName):
	# Removes the placeholder text of the entry
		textvar = self.nameDict[varName]['textvar']

		if textvar.get() == self.nameDict[varName]['placeholder']:
			textvar.set('')
			self.nameDict[varName][str('entryName')].configure(foreground='black')


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
	'''


############################################################################################################################
class ImportColumn:
# Class to handle creation of import instances

	def __init__(self):
	# Create and display everything needed for user to enter import column name
		### Required Variables ###
		self.columnSV = StringVar() # Variable to hold entered column
		self.entryFieldID = ''

		### Interface Setup ###
		self.entryFrame = ttk.Frame(ColumnSelection.mainFrame, padding='3 3') # Frame for easy layout
		self.entryFrame.pack(anchor=W)

		self.vcmd = self.entryFrame.register(EntryHandler.validateColumnEntry) # Register validate command on new frame

		ttk.Label(self.entryFrame, text='Enter name of column to import data from:').grid(columnspan=4, row=0) # Column selection label

		# Column selection entry
		self.columnEntry = ttk.Entry(self.entryFrame, width=17, textvariable=self.columnSV, validate='all', validatecommand=(self.vcmd, '%V', '%W', '%P'))
		self.columnEntry.grid(columnspan=2, column=4, row=0)

		# Add spacing to all widgets within this frame
		for child in self.entryFrame.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

		### Update necessary variables ###
		#if self.columnSV.get()
		ColumnSelection.columnsToImportDict[self.columnSV.get()] = [] # Add column name to dict
		ColumnSelection.columnsToImportDict[self.columnSV.get()].append(self.entryFieldID) 


	def removeImport(self):
	# Remove current import entry
		del self.columnSV
		self.entryFrame.destroy()


############################################################################################################################
class EntryHandler():
# Class to handle various tasks for entry widgets

	def addImport():
	# Add another import entry
		ImportColumn() # Add another button


	def remPlaceholder(self, varName):
	# Removes the placeholder text of the entry
		textvar = self.nameDict[varName]['textvar']

		if textvar.get() == self.nameDict[varName]['placeholder']:
			textvar.set('')
			self.nameDict[varName][str('entryName')].configure(foreground='black')

	
	def validateColumnEntry(self, reason, widgetName, newColumnValue):
	# Called on entry state change, allows or denies edit. Return True to allow edit, False to disallow
		print('Reason: ' + reason + ' Name: ' + widgetName + ' newColumnValue: ' + newColumnValue)

		if reason == 'focusin':
			self.remPlaceholder(varName)

		elif reason == 'focusout':
			self.setPlaceholder(varName, False)

		elif reason == 'key':
			if not self.validateEntry(varName, entryValue):
				return False

			elif (self.nameDict[varName]['type'] == 'pattern') and (ParamSelection.offsetMode.get() == 'char'):
				if entryValue != '':
					self.toggleEnable('en')
				else:
					self.toggleEnable('dis')
		return True	
		pass # Validate data entry


#************************************ Program Start ************************************#
### Create objects ###
filePane = FileSelection()
paramPane = ColumnSelection()

### Run GUI ###
root.mainloop()