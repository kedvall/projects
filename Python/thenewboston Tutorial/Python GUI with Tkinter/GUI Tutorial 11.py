from tkinter import *


def doNothing():
	print('Menu item clicked')

root = Tk() # Main root window (Blank main window)

# ***** Main Menu *****
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

# ***** Toolbar *****
toolbar = Frame(root, bg="blue")

insertButton = Button(toolbar, text="Insert Image", command=doNothing)
insertButton.pack(side=LEFT, padx=2, pady=2)
printButton = Button(toolbar, text="Print", command=doNothing)
printButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

# ***** Status Bar *****
status = Label(root, text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

root.mainloop()