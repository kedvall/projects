import base64
import os
import base64ico
from tkinter import *
##The Base64 icon version as a string
icon = base64ico.icon
icondata= base64.b64decode(icon)
## The temp file is icon.ico
tempFile= "icon.ico"
iconfile= open(tempFile,"wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()
root = Tk()
root.wm_iconbitmap(tempFile)
## Delete the tempfile
os.remove(tempFile)

root.mainloop()