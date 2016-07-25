; AHK Test Script
CoordMode, Mouse, Client

^!c::
	SetTitleMatchMode, 3
	WinActivate, Untitled - Notepad
	Send, Look text 
	Send, {ENTER}