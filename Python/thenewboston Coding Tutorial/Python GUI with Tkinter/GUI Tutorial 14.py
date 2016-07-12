from tkinter import *

root = Tk()

photo = PhotoImage(file="logo.png") # File can be a complete file path
label = Label(root, image=photo)
label.pack()

root.mainloop()