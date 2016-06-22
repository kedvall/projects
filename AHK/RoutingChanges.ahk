SetTitleMatchMode, 2

#IfWinActive Routing -
^+s::
	CoordMode, Mouse, Screen
	Click, 487, 55
	Sleep 500

	Send {DOWN}
	Send {Enter}
	Sleep 250

	Click, 518, 494, 0
	Sleep 500
	Click, right
	Sleep 500
	Click, 541, 533
	Sleep 500

	Send, {Ctrl Down}a{Ctrl Up}
	Send, {BS}	
	Send, STD020
	Sleep 500
	
	Click, 843, 567
	
	SetTitleMatchMode, 3	
Return

#IfWinActive Modify Standard Operation
^+s::
	Send, {Enter}
	Send, {F12}
	SetTitleMatchMode, 2
Return