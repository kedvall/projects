SetTitleMatchMode, 1

#IfWinActive Inventory Part -
^+s::
	SetTitleMatchMode, 3
	WinActivate, InventoryShippingInstructionUpdate.xlsx - Excel
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
	WinActivate, Inventory Part -
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
	WinActivate, Inventory Part -

	CoordMode, Mouse, Client
	Click, right, 559, 81
	Sleep 500
	; Right click main window

	CoordMode, Mouse, Client
	Click, 647, 416
	Sleep 500
	; Open document notes

	Click, 248, 39, 0
	Click 4
	; Open Notes if it's there

	SetTitleMatchMode, 1
Return

#IfWinActive Document Texts for Inventory Part - 
^+s::
	CoordMode, Mouse, Client
	Click, 500, 52
	Sleep 500

	Send, MFGINFO
	Send, {TAB}
	Send, ^v
	Sleep, 250

	CoordMode, Mouse, Client
	Click, 500, 80
	Sleep 500
	Click, 500, 198, 0
Return

#IfWinActive
^+s::
	Send, {ENTER}
	Send, {ENTER}
	Send, ^v
	CoordMode, Mouse, Client
	Click, 368, 29, 0
Return