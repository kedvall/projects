self.msgBoxText = 'You entered the same column to search and paste data to.\nThis will overwrite the search column with new data,\nare you sure you want to proceed?'


self.overwriteCheck()




def overwriteCheck(self):
	if ParamSelection.searchCol.get() == ParamSelection.pasteCol.get():
		ans = tkinter.messagebox.askquestion('Overwrite Confirmation', self.msgBoxText, parent=self.paramFrame)
		if ans == 'no':
			ParamSelection.pasteCol.set('')
			self.pColEntry.configure(foreground='black')
			self.pColEntry.focus()