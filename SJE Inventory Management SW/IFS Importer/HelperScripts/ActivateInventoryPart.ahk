#Persistent
#SingleInstance, force

SetTitleMatchMode, 2

if WinExist("Inventory Part -")
	WinActivate, Inventory Part -
else
	MsgBox, 48, IFS Error, Inventory Part window is not active in IFS`nPlease navigate to Inventory Part then try again, 6

ExitApp