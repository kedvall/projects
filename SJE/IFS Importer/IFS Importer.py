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
		

#************************************ Program Start ************************************#
# Create objects
filePane = FileSelection()

# Run GUI
root.mainloop()