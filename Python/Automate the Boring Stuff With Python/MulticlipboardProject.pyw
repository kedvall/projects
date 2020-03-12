#! python3
# .pyw extension means no terminal window will be shown when this program runs

# Multi clipboard program - Saves and loads pieces of text to the clipboard
# Usage: py.exe MulticlipboardProject.pyw save <keyword> - Saves clipboard to the keyword
#		 py.exe MulticlipboardProject.pyw <keyword> - Loads keyword to the clipboard
#		 py.exe MulticlipboardProject.pyw list - Loads all keywords to the clipboard

# Program functions:
# 	- Command line argument for keyword is checked
#	- If argument is save, clipboard contents are saved to keyword
#	- If argument is list, all keywords are copied to clipboard
#	- Otherwise, text for the keyword is copied to the clipboard

import shelve, pyperclip, sys

mcbShelf = shelve.open('mcb')

# Save clipboard content
if len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
	mcbShelf[sys.argv[2]] = pyperclip.paste()

elif len(sys.argv) == 2:
	# List keywords and load content
	if sys.argv[1].lower() == 'list':
		pyperclip.copy(str(list(mcbShelf.keys())))
	elif sys.argv[1] in mcbShelf:
		pyperclip.copy(mcbShelf[sys.argv[1]])
		
mcbShelf.close()