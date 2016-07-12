#! python3
from tkinter import *

root = Tk()

def printNameCmd():
	print("Hello world! Cmd")

def printNameEvent(event):
	print("Hello world! Event")

button_1 = Button(root, text="Print my name", command=printNameCmd)
button_1.pack()

button_2 = Button(root, text="Print my name")
button_2.bind("<Button-1>", printNameEvent)
button_2.pack()

root.mainloop()