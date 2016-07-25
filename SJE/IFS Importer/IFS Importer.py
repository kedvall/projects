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


# Auto Hotkey Test
ahk_interpreter = Interpreter() # Create an ahk interpreter

ahk_script = '''
	CoordMode, Mouse, Client

	!^c::
		SetTitleMatchMode, 3
		WinActivate, Untitled - Notepad
		Send, Look text 
		Send, {ENTER}
			'''

ahk_interpreter.execute_script(ahk_script) # Start a thread in the interpreter that runs the script

while 1:
    cmd = input('quit - quit the program\n Press CTRL+ALT+c\n')
    if cmd.lower() == 'quit':
        break
ahk_interpreter.terminate() # Terminate the running script


root.mainloop()