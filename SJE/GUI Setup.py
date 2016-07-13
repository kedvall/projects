from tkinter import *
from tkinter import ttk, filedialog
import tkinter.messagebox

# Set up GUI
root = Tk() # Create blank window
root.title("Excel Data Scraper") # Set the name
style = ttk.Style()


# Class declaration
class FileSelection:
	# File Selection Frame (Upper left)
	def __init__(self):
		# Frame setup
		fileFrame = ttk.Frame(root, padding="3 3 12 12") # Make a themed frame to hold objects
		fileFrame.grid(column=0, row=0, sticky=(N, W, E, S))
		fileFrame.columnconfigure(0, weight=1)
		fileFrame.rowconfigure(0, weight=1)

		# Required variables
		self.filePath = StringVar()
		self.selectedSheet = StringVar()
		self.fileDisp = StringVar()

		# File opening options
		self.fileOpt = options = {}
		options['defaultextension'] = '.xlsx'
		options['filetypes'] = [('Excel', '.xlsx'), ('Spreadsheet', '.xlsm'), ('Spreadsheet', '.xltx'), ('Spreadsheet', '.xltm'), ('All Files', '.*')]
		options['initialdir'] = 'C:\\Users\\intern\\Documents'
		options['parent'] = fileFrame
		options['title'] = "Select a File to Use"

		# Interface elements
		self.fileBtn = ttk.Button(fileFrame, text='Select File:', style='fileBtn.TButton')
		self.fileBtn.bind('<Button-1>', self.askDir)
		self.fileBtn.grid(columnspan=2, row=1, sticky=E)
		self.fileEntry = ttk.Entry(fileFrame, width=50, textvariable=self.filePath)
		self.fileEntry.grid(columnspan=3, column=3, row=1, sticky=W)

		ttk.Label(fileFrame, text="Select Sheet:").grid(columnspan=2, row=2, sticky=E)
		self.sheetCBox = ttk.Combobox(fileFrame, textvariable=self.selectedSheet, state='readonly')
		self.sheetCBox.bind('<<ComboboxSelected>>', self.doSomething)
		self.sheetCBox['values'] = ('Sheet1', 'Sheet2', 'Sheet3')
		self.sheetCBox.current(0)
		self.sheetCBox.grid(columnspan=3, column=3, row=2, sticky=W)

		self.loadBtn = ttk.Button(fileFrame, text="Load File", style='loadBtn.TButton')
		self.loadBtn.state(['disabled'])
		self.loadBtn.bind('<Button-1>', self.loadFile)
		self.loadBtn.grid(columnspan=2, row=3)
		ttk.Label(fileFrame, textvariable=self.fileDisp).grid(columnspan=3, column=3, row=3, sticky=W)

		for child in fileFrame.winfo_children(): child.grid_configure(padx=5, pady=15)

	def doSomething(self, event):
		print('Box moved')

	def loadFile(self, event):
		self.fileDisp.set('Successfully loaded: ' + str(self.filePath.get()))
		print('File Loaded!!!')

	def askDir(self, event):
		self.filename = filedialog.askopenfilename(**self.fileOpt)
		if self.filename:
			self.filePath.set(self.filename)
		style.configure('fileBtn.TButton', relief=RAISED)
		self.loadBtn.state(['!disabled'])






upperLeftPane = FileSelection()

root.mainloop()