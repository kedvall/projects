from tkinter import *

master = Tk()
listbox = Listbox(master, selectmode=MULTIPLE)
listbox.pack()

listbox.insert(END, "a list entry")

for item in ['one', 'two', 'three', 'four']:
	listbox.insert(END, item)

for number in range(1, 125):
	listbox.insert(END, str(number))

mainloop()