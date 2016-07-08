/******************************************************************************************************************************************
 	Excel to IFS Template
	Written by Kanyon Edvall

	This is a template for scripts to intelligently move data from Excel to IFS
		Code here should serve as a base that can be easily modified for a particular task
		An example is also included (at bottom)

	Common Commands:
	- SetTitleMatchMode: Changes how a search for a window title is performed (more on this later)
	- WinActivate: Sets focus to the specified window based on window title
	- #IfWinActive: Checks the currently focused window and executes appropriate code
		Useful for making window (application) specific hotkeys 
		Behaves like IF statement, allowing certain code to be executed based on active window
	- Send: Sends a keystroke or set of keystroke (emulates typing on the keyboard)
		Standard keys: a, b, c, etc
		Special keys: {Enter}, {Tab}, {F3}, {Right} (right arrow key), etc
		Control keys: A key prefixed by ^ is Ctrl + KEY. For example: ^c (copy), ^v (paste), ^a (select all)
	- Sleep: Inserts a delay (in milliseconds) into the program's execution
		Useful when a menu is activated and doesn't instantly appear (mouse needs to move/click slower)
		or when keystrokes need to be sent slower (moving in excel using arrow keys)
	- CoordMode: Changes how the mouse moves, use in conjunction with Active Window Info (Window Spy)
		Client, Window, and Screen correspond to the different coordinates on Window Spy (Client, Relative, and Absolute)
			Client: Coordinates are relative to the current window (excluding the title bar and boarders) (Usually preferred)
			Window: Coordinates are relative to the current window (including title bar and boarders)
			Screen: Coordinates are relative to the entire screen, these are absolute coordinates (Avoid this if possible)
	- Click: Moves mouse pointer and optionally clicks (emulates a mouse)
		Coordinates, right/left/middle click, and number of clicks can be specified 
		For example: Click, right, 400, 500, 2
			Right clicks the mouse at (400, 500) twice (double click)
	- Return: Ends the current set of commands (typically stops execution until another key is pressed)
		IMPORTANT, commands will keep executing unless you end you code block with this

	Other Important Features:
	- Hotkeys: Hotkeys are the keys pressed to trigger a block of code to run. This is how the program is told when to execute
		Syntax: MODIFIER(S) + KEY(S):: 
		- MODIFIER(S) are special keys such as Ctrl, Shift, and Alt
			^ signifies Ctrl, + signifies Shift, and ! signifies Alt
		- KEY(S) are any other key or keys that must also be pressed simultaneously, use lowercase keys
		- All hotkeys end with ::
		For example: ^+s:: means Ctrl Shift S, ^!d:: means Ctrl Alt D
	- Comments: Comments have no affect on the program's execution, they are simply for clarity and to help others understand your program
		Syntax: ; COMMENT
		- All comments start with ;
		- Anything can go after ; and is considered a comment
		- Comments can be on their own separate line or after a line of code
		- For example: SetTitleMatchMode, 1 ; Here is a comment describing what this line does
******************************************************************************************************************************************/


/******************************************************************************************************
* TEMPLATE, see below for complete commented example:												  *
******************************************************************************************************/
SetTitleMatchMode, 1

#IfWinActive IFSWINDOWNAMEHERE
^+s::
	SetTitleMatchMode, 3
	WinActivate, EXCELFILENAMEHERE.xlsx - Excel
	Send, {RIGHT}
	Send, X
	Sleep 300
	Send, {LEFT}
	Sleep 300
	Send, ^c
	Send, {DOWN}
	Sleep 300
	; Check off adjacent Excel block and copy inventory number

	SetTitleMatchMode, 3
	WinActivate, IFSWINDOWNAMEHERE
	Send, {F3}
	Send, ^v
	Send, {Enter}
	Sleep 500
	; Search for part based on number from Excel

	SetTitleMatchMode, 3
	WinActivate, Untitled - Notepad
	Send, ^a
	Send, ^c
	; Switch to Notepad, copy all text

	SetTitleMatchMode, 2
	WinActivate, IFSWINDOWNAMEHERE
	; Back to IFS

	CoordMode, Mouse, Client
	Click, COORDSHERE
	Sleep 500
	; Move mouse and wait for menu

	SetTitleMatchMode, 1
	; Go back to exact title matching
Return

#IfWinActive SPECIFICIFSWINDOW
^+s::
	CoordMode, Mouse, Client
	Click, COORDSHERE
	Sleep 500
	; Move mouse, wait for menu

	Send, KEYSTROKES
	Send, {TAB}
	Send, ^v
	Sleep, 250
	; Send keystrokes, tab over, and paste text from Notepad

	CoordMode, Mouse, Client
	Click, COORDSHERE
	Sleep 500
	Click, COORDSHERE, 0
	; Click Save and hover mouse over Close
Return

#IfWinActive
^+s::
	Send, KEYSTROKES
	Send, ^v
	CoordMode, Mouse, Client
	Click, COORDSHERE, 0
	; Send keystrokes, paste text from Notepad, hover over Save
Return


 /******************************************************************************************************
 * EXAMPLE complete with comments 																	   *
 * This script creates or appends a MFGINFO field in IFS and pasts arbitrary text from Notepad into it *
 ******************************************************************************************************/
; Look for window with title that STARTS WITH the specified string
SetTitleMatchMode, 1 

; Execute the below code only if a window starting with Inventory Part - is active
#IfWinActive Inventory Part -
; Hotkey to activate code, in this case Ctrl Shift s (All pressed simultaneously)
^+s::
	; Look for window with title that EXACTLY MATCHES the specified string
	SetTitleMatchMode, 3
	; Set focus to the specified window
	WinActivate, InventoryShippingInstructionUpdate.xlsx - Excel
	; Send right arrow key
	Send, {RIGHT}
	; Send the X key
	Send, X
	; Wait 300 milliseconds
	Sleep 300
	Send, {LEFT} 
	Sleep 300
	; Send Ctrl + c for copy
	Send, ^c
	Send, {DOWN}
	Sleep 500
	; The above block of code puts an X in the adjacent cell, copies the text, and moves down a cell

	SetTitleMatchMode, 1
	WinActivate, Inventory Part -
	; Send F3 (function key at top of keyboard)
	Send, {F3}
	; Send Ctrl + v for paste
	Send, ^v
	; Send ENTER key
	Send, {Enter}
	Sleep 500
	; The above code searches for a part number in IFS based on the part number copied from Excel

	SetTitleMatchMode, 3
	WinActivate, Untitled - Notepad
	Send, ^a
	Send, ^c
	; The above code switches to Notepad, and copies all text in it

	SetTitleMatchMode, 1
	WinActivate, Inventory Part -
	; The above code block switches focus back to an IFS window starting with Inventory Part -

	; Set mouse movement to use coordinates in Client mode (coordinates are relative the current window excluding title bar and boarder)
	CoordMode, Mouse, Client
	; Right click mouse at coordinates (559, 81)
	Click, right, 559, 81
	Sleep 500
	; The above code moves the mouse to the specified coordinates and right clicks to display a menu

	CoordMode, Mouse, Client
	Click, 647, 416
	Sleep 500
	; The above code moves to an item on the list (in this case Document Notes) and clicks it

	; Move mouse to specified coordinates and click 0 times (Just move mouse, don't click it)
	Click, 248, 39, 0
	; Click the left mouse button 4 times (If coordinates are omitted, a single number refers to # of clicks. Otherwise, click count goes after the set of coordinates)
	Click 4
	; The above code moves the mouse to where a MFGINFO item would be and quadruple clicks to open the large editor to append text

	SetTitleMatchMode, 1
; End of code block, stop executing
Return

; Look for a window starting with Document Texts for Inventory Part - 
#IfWinActive Document Texts for Inventory Part - 
; Same hotkey (Ctrl Shift s), but only works if the windows currently focused has the above name
^+s::
	CoordMode, Mouse, Client
	Click, 500, 52
	Sleep 500
	; The above code moves the mouse over the New button on Document Notes and clicks it to add a field

	Send, MFGINFO
	Send, {TAB}
	Send, ^v
	Sleep, 250
	; The above code types MFGINFO, hits Tab to go to the next field, and pastes the text copied from Notepad

	CoordMode, Mouse, Client
	Click, 500, 80
	Sleep 500
	Click, 500, 198, 0
	; The above code clicks the Save button on the Documents Notes windows, then hovers over the Close button
; End of code block, stop executing
Return

; If the currently focused window has no title or does match an #IfWinActive statement this code will execute
#IfWinActive
; Still same hotkey (Ctrl Shift s), but only works if the window currently focused does not match a specified #IfWinActive statement
; Think of this a "global" hotkey that will work in any window not specified by a #IfWinActive statement
^+s::
	Send, {ENTER}
	Send, {ENTER}
	Send, ^v
	CoordMode, Mouse, Client
	Click, 368, 29, 0
	; The above code appends an existing MFGINFO field by inserting a blank line, then pasting the text from Notepad at the end of the existing MFGINFO instructions
	; The mouse then hovers over the same button but does not click it (So it can be check for accuracy before being saved)
; End of code block, stop executing
Return