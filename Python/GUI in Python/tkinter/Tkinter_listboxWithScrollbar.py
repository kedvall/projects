from tkinter import *

master = Tk()
frame = Frame(master)
listbox = Listbox(frame)

scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack() #(side=LEFT, fill=BOTH, expand=1)
frame.pack()

listbox.insert(END, "a list entry")

for item in ['one', 'two', 'three', 'four']:
	listbox.insert(END, item)

for number in range(1, 125):
	listbox.insert(END, str(number))

mainloop()