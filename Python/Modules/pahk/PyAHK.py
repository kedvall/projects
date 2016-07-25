#! python3

from pahk import Interpreter

ahk_interpreter = Interpreter() # Create an ahk interpreter
ahk_script = '^h::MsgBox Hello'  #An ahk script. If Ctrl+c is pressed, brings a msgbox
ahk_interpreter.execute_script(ahk_script) # Start a thread in the interpreter that run the script

while 1:
    cmd = input('quit - quit the program\n Press CTRL+H to say hello!\n')
    if cmd.lower() == 'quit':
        break