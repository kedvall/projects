Rem Shebang protocols:
Rem Windows:	#! python3
Rem OSX:		#! /usr/bin/env python3
Rem Linux: 		#! /usr/bin/python3

Rem pyw is windowless, no execution window is displayed
Rem %* forwards any command line arguements to the program

@py.exe C:\path\to\your\pythonScript.py %*
@pause