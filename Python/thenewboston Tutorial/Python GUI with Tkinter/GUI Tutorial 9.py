from tkinter import *


def doNothing():
	print('Menu item clicked')

root = Tk() # Main root window (Blank main window)

menuBar = Menu(root)
root.config(menu=menuBar)

subMenu = Menu(menuBar) # Create submenu
menuBar.add_cascade(label="File", menu=subMenu) # Add dropdown menu

subMenu.add_command(label="New Project...", command=doNothing) # Add clickable object to submenu
subMenu.add_command(label="New...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

editMenu = Menu(menuBar)
menuBar.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=doNothing)

root.mainloop()