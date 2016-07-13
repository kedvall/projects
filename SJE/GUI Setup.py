from tkinter import *
from tkinter import ttk, filedialog
import tkinter.messagebox

someText = "Some text"

def doSomething(event):
	print('Box moved')

def loadFile(event):
	fileDisp.set('Successfully loaded: ' + str(filePath.get()))
	print('File Loaded!!!')

def askDir(event):
	filename = filedialog.askopenfilename(**fileOpt)
	if filename:
		filePath.set(filename)
	style.configure('fileBtn.TButton', relief=RAISED)
	loadBtn.state(['!disabled'])

# Set up GUI
root = Tk() # Create blank window
root.title("Excel Data Scraper") # Name it
style = ttk.Style()

### File Selection Frame (Upper left) ###
# Frame setup
fileFrame = ttk.Frame(root, padding="3 3 12 12") # Make a themed frame to hold objects
fileFrame.grid(column=0, row=0, sticky=(N, W, E, S))
fileFrame.columnconfigure(0, weight=1)
fileFrame.rowconfigure(0, weight=1)

# Required variables
filePath = StringVar()
selectedSheet = StringVar()
fileDisp = StringVar()

# File opening options
fileOpt = options = {}
options['defaultextension'] = '.xlsx'
options['filetypes'] = [('Excel', '.xlsx'), ('Spreadsheet', '.xlsm'), ('Spreadsheet', '.xltx'), ('Spreadsheet', '.xltm'), ('All Files', '.*')]
options['initialdir'] = 'C:\\Users\\intern\\Documents'
options['parent'] = fileFrame
options['title'] = "Select a File to Use"

# Interface elements
fileBtn = ttk.Button(fileFrame, text='Select File:', style='fileBtn.TButton')
fileBtn.bind('<Button-1>', askDir)
fileBtn.grid(columnspan=2, row=1, sticky=E)
fileEntry = ttk.Entry(fileFrame, width=50, textvariable=filePath)
fileEntry.grid(columnspan=3, column=3, row=1, sticky=W)

ttk.Label(fileFrame, text="Select Sheet:").grid(columnspan=2, row=2, sticky=E)
sheetCBox = ttk.Combobox(fileFrame, textvariable=selectedSheet, state='readonly')
sheetCBox.bind('<<ComboboxSelected>>', doSomething)
sheetCBox['values'] = ('Sheet1', 'Sheet2', 'Sheet3')
sheetCBox.current(0)
sheetCBox.grid(columnspan=3, column=3, row=2, sticky=W)

loadBtn = ttk.Button(fileFrame, text="Load File", style='loadBtn.TButton')
loadBtn.state(['disabled'])
loadBtn.bind('<Button-1>', loadFile)
loadBtn.grid(columnspan=2, row=3)
ttk.Label(fileFrame, textvariable=fileDisp).grid(columnspan=3, column=3, row=3, sticky=W)


for child in fileFrame.winfo_children(): child.grid_configure(padx=5, pady=15)
root.mainloop()