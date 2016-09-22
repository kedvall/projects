SetTitleMatchMode, 2
#IfWinActive  - Mozilla Firefox
^+d::
	Send, ^d
	Sleep 750
	CoordMode, Mouse, Client
	MouseMove, 1632, 196
	Click
	Sleep 500
	MouseMove, 1550, 326
	Click
	Sleep 500
	Send, {Enter}
	Send, ^w
	Sleep 500
Return