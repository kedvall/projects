#! python3

import pyperclip

text = str(pyperclip.paste())
key = ""

text = text.split('"')
key = 'reg delete "' + text[1] + '" /ve /f'
print(key)

pyperclip.copy(key)