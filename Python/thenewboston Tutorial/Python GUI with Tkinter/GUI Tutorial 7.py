#! python3

from tkinter import *

root = Tk()

def leftClick(event):
	print("Left")

def middleClick(event):
	print("Middle")

def rightClick(event):
	print("Right")

def scroll(event):
	print("Scroll")

frame = Frame(root, width=300, height=250) # Makes the window 300 x 250
frame.bind("<Button-1>", leftClick) # Frame is technicall a widget, can bind to it
frame.bind("<Button-2>", middleClick)
frame.bind("<Button-3>", rightClick)
frame.bind("<MouseWheel>", scroll)

frame.pack()

root.mainloop()