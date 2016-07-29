#Persistent

searchText = EDIT
pgrmStatus = running

parseText(textToSearch)
{
	global 
	IfInString, textToSearch, %searchText% 
	{
		selectionState = ## VALID ## entry field
		return true
	}

	selectionState = ## INVALID ## (must be entry field)
	return false
}


Start:
	SetTimer, WatchCursor, 100
return

WatchCursor:
	MouseGetPos, , , id, control
	WinGetTitle, title, ahk_id %id%
	ToolTip, %selectionState%`nHold Ctrl and click in the desired entry field`nWindow Title: %title%`nEntry Field ID: %control%
	parseText(control)
return

^LButton::
	if (parseText(control))
	{
		SetTimer, WatchCursor, Off
		Tooltip
		goto, processInput
	}

	else
	{
		MsgBox, Not a valid entry field!`nAre you sure you clicked an entry field?
	}
return

processInput:
	selectionInfo = %title%|%control%
	pgrmStatus = done
	MsgBox, Successfully added %selectionInfo%
	ExitApp