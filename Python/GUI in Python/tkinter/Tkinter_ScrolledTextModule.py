import tkinter
from tkinter.scrolledtext import *
 
root = tkinter.Tk(className=" Another way to create a Scrollable text area")
textPad = ScrolledText(root, width=50, height=40)
textPad.pack()
root.mainloop()