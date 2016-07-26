script = '''
CoordMode, Mouse, Client
^!c::
	SetTitleMatchMode, 3
	WinActivate, Untitled - Notepad
	Send, Look text 
	Send, {ENTER}
'''


# Auto Hotkey Test
ahk_interpreter = Interpreter()
ahk_script = script
ahk_interpreter.execute_script(ahk_script)

print('Executing')
for i in range(1,6):
	pyautogui.keyDown('ctrl')
	pyautogui.keyDown('alt')
	pyautogui.keyDown('c')
	pyautogui.keyUp('ctrl')
	pyautogui.keyUp('alt')
	pyautogui.keyUp('c')
	print(i)

print('Done, quitting.')