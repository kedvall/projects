#SingleInstance, force

Loop
{
	; Find ID of control beneath mouse
	MouseGetPos, , , id, control

	; Check if EDIT is in the control ID
	IfInString, control, EDIT
	{
		selectionState = ## VALID ## (entry field found)
		Suspend, Off
	}
	
	IfNotInString, control, EDIT
	{
		selectionState = No valid entry field found
		Suspend, On
	}

	; Set tool tip based on control ID
	ToolTip, %selectionState%`nHold Ctrl and click in the desired entry field

} Until breakLoop = 1

Clipboard = %control%
Sleep, 100

ExitApp

~^Lbutton::
	breakLoop = 1
	return

+Esc::
	Suspend, Permit
	breakLoop = 1
	ExitApp