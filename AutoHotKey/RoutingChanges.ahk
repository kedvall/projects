SetTitleMatchMode, 2

#IfWinActive Routing -
^+s::
	CoordMode, Mouse, Client
	Click, 586, 28
	Sleep 500
	Click, WD
	Click, 61, 34
	Sleep 500

	Click, right, 228, 69
	Sleep 100
	Click, 657, 502
	
	Send, STD020

	ControlFocus, WindowsForms10.BUTTON.app.0.2780b98_r14_ad14
	Click	
	
	SetTitleMatchMode, 3	
Return

#IfWinActive Modify Standard Operation
^+s::
	Send, {Enter}
	Send, {F12}
	SetTitleMatchMode, 2
Return