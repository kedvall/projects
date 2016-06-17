^j::
	MsgBox Wow!
	MsgBox this is
	Run, Notepad.exe
	winactivate, Untitled - Notepad
	WinWaitActive, Untitled - Notepad
	send, 7 lines{!}{enter}
	sendinput, inside the ctrl{+}j hotkey 
Return

::exp::Expanding text is magical!


::btw::
	MsgBox You typed "btw".
Return


Numpad0 & Numpad1::
	MsgBox You pressed Numpad1 while holding down Numpad0
Return


Numpad0 & Numpad2::
	Run Notepad
Return