!`::
Send, ^s

SetTitleMatchMode, 3
WinActivate, Data.xlsx - Excel
Send, ^c{DOWN} 
; Got down a cell in Excel

SetTitleMatchMode, 2
WinActivate, Inventory Part
Send, {F3}
Send, ^v
Send, {Enter}
Sleep 500

ControlFocus, WindowsForms10.EDIT.app.0.2780b98_r14_ad18, Inventory Part
Click
Sleep, 300

Return


;;Text Boxes
; WindowsForms10.EDIT.app.0.2780b98_r14_ad18
; WindowsForms10.EDIT.app.0.2780b98_r14_ad19
; WindowsForms10.EDIT.app.0.2780b98_r14_ad16
; WindowsForms10.EDIT.app.0.2780b98_r14_ad17