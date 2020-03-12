#! python3
# .pyw extension means no terminal window will be shown when this program runs

# Extended multi clipboard program - Saves and loads pieces of text to the clipboard
# Usage: py.exe mcbExt.pyw save <keyword> - Saves clipboard to the keyword
#		 py.exe mcbExt.pyw delete <keyword> - Deletes the keyword
#		 py.exe mcbExt.pyw <keyword> - Loads keyword to the clipboard
#		 py.exe mcbExt.pyw list - Loads all keywords to the clipboard
#		 py.exe mcbExt.pyw delete - deletes ALL keywords resetting the list

import shelve, pyperclip, sys

mcbShelf = shelve.open('mcb')

if len(sys.argv) == 3:
	# Save clipboard content
	if sys.argv[1].lower() == 'save':
		mcbShelf[sys.argv[2]] = pyperclip.paste()
	# Delete keyword entry
	if sys.argv[1].lower() == 'delete':
		del mcbShelf[sys.argv[2]]

elif len(sys.argv) == 2:
	# List keywords and load content
	if sys.argv[1].lower() == 'list':
		pyperclip.copy(str(list(mcbShelf.keys())))
	# Delete ALL keywords (reset clipboard)
	if sys.argv[1].lower() == 'delete':
		mcbShelf.clear()
	# Copy text for keyword to clipboard
	elif sys.argv[1] in mcbShelf:
		pyperclip.copy(mcbShelf[sys.argv[1]])
		
mcbShelf.close()