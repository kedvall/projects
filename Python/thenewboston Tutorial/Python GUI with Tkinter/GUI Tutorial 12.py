from tkinter import *
import tkinter.messagebox

root = Tk()

# Static dialog
tkinter.messagebox.showinfo('Window Title', 'Message box text!')

# Interactive button
answer = tkinter.messagebox.askquestion('Question 1', 'Respond yes or no.')

if answer == 'yes':
	print('You answered yes!')
else:
	print('You answered no!')

root.mainloop()