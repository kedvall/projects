 #! python3
from pahk import Interpreter
from time import sleep

def input_box(title,prompt):
    
    script = '''
    #Persistent
    title = %1%
    Prompt = %2%
    rep = None
    InputBox, rep, %title%,%Prompt%
    '''

    ahk_interpreter = Interpreter()
    ahk_script = script
    ahk_interpreter.execute_script(ahk_script,param = '{0} {1}'.format(title,prompt))
    sleep(0.5)
    
    while ahk_interpreter.var_get('rep') == 'None':
        sleep(0.2)
    
    rep = ahk_interpreter.var_get('rep')
    
    ahk_interpreter.terminate()
    del ahk_interpreter
    
    return rep

while 1:
    rep = input_box(title = '"Python"', prompt = '"Enter something"')
    if rep == 'quit':
        break
    print(rep)