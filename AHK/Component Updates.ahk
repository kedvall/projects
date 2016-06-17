SetTitleMatchMode, 2

#IfWinActive - IFS Applications
^+s::
	SetTitleMatchMode, 3
	WinActivate, ComponentUpdates.xlsx - Excel
	Send, {RIGHT}
	Send, X
	Sleep 300
	Send, {LEFT}
	Sleep 300
	Send, ^c
	Send, {DOWN}
	Sleep 500
	; Go down a cell in Excel

	SetTitleMatchMode, 2
	WinActivate, Inventory Part
	Send, {F3}
	Send, ^v
	Send, {Enter}
	Sleep 500
	; Bring up part based on excel part number

	SetTitleMatchMode, 3
	WinActivate, Untitled - Notepad
	Send, ^a
	Send, ^c
	; Switch to notepad, copy all text

	SetTitleMatchMode, 2
	WinActivate, Inventory Part

	CoordMode, Mouse, Client
	Click, 1887, 446
	Sleep 500
	; Click sidebar
	CoordMode, Mouse, Client
	Click, 151, 408
	Sleep 500
	; Open document notes

	Click, 248, 39, 0
	Click 4
	
	SetTitleMatchMode, 2
Return

#IfWinActive Document Texts for Inventory Part - 
^+s::
	CoordMode, Mouse, Client
	Click, 501, 51
	Sleep 500

	Send, MFGINFO
	Send, {TAB}
	Send, ^v

	CoordMode, Mouse, Client
	Click, 492, 79
	Sleep 500
	Click, 497, 195, 0
Return

#IfWinActive
^+s::
	Send, {ENTER}
	Send, {ENTER}
	Send, ^v
	CoordMode, Mouse, Client
	Click, 372, 28, 0
Return