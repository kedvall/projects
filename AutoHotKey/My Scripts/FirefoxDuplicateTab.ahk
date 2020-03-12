SetTitleMatchMode, 2

#IfWinActive - Mozilla Firefox
!d::
	Send, ^l
	Sleep, 250
	Send, ^c 
	Send, ^t 
	Sleep, 250
	Send, ^v
	Send, {ENTER}