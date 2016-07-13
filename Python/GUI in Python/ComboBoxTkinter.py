from tkinter import *
from tkinter import ttk

root = Tk()

def printSomething(event):
	print('Box moved')

countryvar = StringVar()
country = ttk.Combobox(root, textvariable=countryvar)
country.bind('<<ComboboxSelected>>', printSomething)
country['values'] = ('USA', 'Canada', 'Australia')
country.current(0)

country.pack()

root.mainloop()