#! python3

from tkinter import *

# Main window
root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text="Button1", fg="red") # fg is optional
button2 = Button(topFrame, text="Button2", fg="blue")
button3 = Button(topFrame, text="Button3", fg="green")
button4 = Button(bottomFrame, text="Button4", fg="purple")

button1.pack(side=LEFT) #By default on top
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack()

# Run continuously (keep windows displaying)
root.mainloop()