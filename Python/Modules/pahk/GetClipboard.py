#! python3
from pahk import Interpreter
from time import sleep
    
def get_clipboard():
    ahk_interpreter = Interpreter()
    ahk_script = '''#Persistent\nx = %clipboard%''' # Create a variable "x" which hold the clipboard data.
    ahk_interpreter.execute_script(ahk_script)
    sleep(0.5) #Let the thread warms up
       
    clipboard = ahk_interpreter.var_get('x') #Get the value of the variable x in the current running script
        
    ahk_interpreter.terminate() # Terminate the running script
    del ahk_interpreter
    
    return clipboard 
   
print (get_clipboard())
sleep(30)