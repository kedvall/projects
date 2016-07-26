; From: https://autohotkey.com/board/topic/122108-capturing-data-from-window-spy/
; AHK WinInfo Script 1

#NoEnv
#SingleInstance Force
Menu,Tray,Icon,AU3_Spy.exe
OnExit CloseWindowSpy
Run, AU3_Spy.exe
WinWait, Active Window Info
SetTimer, ShowToolTip, 100
SetTimer, ExitAppl, 500
return

F1:: WinActivate, Active Window Info

F2::
SetTimer, ShowToolTip, off
ClipSaved := ClipboardAll
Clipboard = 
Gui,Destroy
ToolTip, Click anywhere to save the mouse coordinates
KeyWait, LButton, D
WinGetText, text, Active Window Info
Clipboard = %text%
Sleep, 100
Send, {LButton Up}
ToolTip
WinMinimize, Active Window Info
Gui, -Caption
Gui,Font, s10
Gui,Add, Text,, %Clipboard%
Gui,Show, AutoSize, GuiWindow
Sleep, 300
WinGetPos,,,Width,Height, GuiWindow
Gui,Destroy
Sleep, 300
Gui,Font, s10
Gui,Add, Edit, h%Height% w%Width%
Gui,Show, x0 y40 h%Height% w%Width%, WinInfo
Send, ^v
Sleep, 300
Clipboard := ClipSaved
return

GuiClose:
Gui,Destroy
WinRestore, Active Window Info
SetTimer, ShowToolTip, on
return

CloseWindowSpy:
Esc::
WinClose, Active Window Info
ExitApp
return

ShowToolTip:
ToolTip,Press F1 to freeze display`nPress F2 to save the text`nPress Esc to close Window Spy
return

ExitAppl:
IfWinNotExist, Active Window Info
ExitApp
return