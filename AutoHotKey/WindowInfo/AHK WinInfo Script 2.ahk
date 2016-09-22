; From: https://autohotkey.com/board/topic/43893-simple-ahk-window-spy-with-a-user-friendly-interface/
; AHK WinInfo Script 2


; Ahk Window Spy, Uses RCtrl - F11 and  RCtrl - F12

/*
RCtrl - F11  Enables Window Spy which displays
a Tooltip showing the Window Parameters beneath
the mouse pointer.

RCtrl - F12  Disables Window Spy, Removes the Tooltip
and Displays a DropDownList of the parameters returned.
You can then select the parameter you need from the
List and it will be returned to you on the Windows Clipboard.

If you need more than one item from the DropDownList,
Pressing RCtrl - F12  again allows you to grab another
parameter from the list.

The Basic Routine which grabs the Windows Information
and displays the Tooltip came from the AutoHotKey Help File.
This script just gives you a more user-friendly way of exctracting
the information you need for later use.
*/
ParseText(textVar)
{
	searchText = EDIT
	IfInString, textVar, %searchText%
	{
		Msgbox, String Found!
		return
	}
}


#singleinstance force
Start:
SetTimer, WatchCursor, 100
return

WatchCursor:
	MouseGetPos, , , id, control
	WinGetTitle, title, ahk_id %id%
	WinGetClass, class, ahk_id %id%
	ToolTip, ahk_id %id%`nahk_class %class%`n%title%`nControl: %control%
	ParseText(control)
	data1 = ahk_class %class%|ahk_id %id%|%title%|Control: %control%
return

^F12::
	SetTimer, WatchCursor, Off
	ToolTip
	gosub, DDL
return

DDL:
	width = 0
	Loop, 4
	{
		if (strlen(data1) > width)
		   width := strlen(data1)
	}
	width := Round(strlen(data1) * 4.4) ; Attempt to Determine width needed by DropDownList
	StringReplace, data, data1, |, ||  ; Make 1st item in List Default Selection
	Gui, +AlwaysOnTop +ToolWindow
	Gui, font, s11, Arial
	Gui, Add, DropDownList, % "x20 y15 R4 w" . width . " gGrabit vWindata", %data%
	Gui, Show, % "h50 w" . width + 40
Return

Grabit:
	Gui, Submit
	sleep, 100
	clipboard = %Windata%
	GuiClose:
	GuiEscape:
	Gui, Destroy
return