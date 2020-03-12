; Notepad
#IfWinActive Untitled - Notepad
#space::
	MsgBox, You pressed Win+Spacebar in Notepad.
Return
::msg::You typed msg in Notepad
#IfWinActive

; Any other window
#IfWinActive
#space::
	Msgbox, You pressed Win+Spacebar in any other Window.
Return

