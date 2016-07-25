#!/usr/bin/env python

"""XBeeModem.py bypasses the XBee's 802.15.4 capabilities and simply uses it for modem cummunications

	Reference Materials:
		Non-blocking read for stdin in python - http://repo.linux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-python/
		Non-blocking read on a subprecess.PIPE in python - http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
"""

#Imported modules
import os 			#Portable way of using operating system dependant functions
import sys 			#Provides access to some variables used or maintained by the interperter
import time			#Provides various real time functions
import fcntl		#Performs file control and I/O control on file descriptors
import serial		#Encapsulates the access for the serial port
from pretty import switchColor, printc	#Provides colored text for xterm & VT100 type terminals using ANSI escape sequences

#Text colors to be used during terminal sessions
ERROR_TEXT = 'bright red'
CMD_INPUT_TEXT = 'normal'
CMD_OUTPUT_TEXT = 'bright yellow'
TERM_OUTPUT_TEXT = 'purple'
TERM_INPUT_TEXT = 'bright purple'

#Setup
if __name__ == '__main__':
	serial = serial.Serial()
	serial.port = '/dev/ttyUSB0'
	serial.baudrate = 9600
	serial.timeout = 1
	serial.writeTimeout = 1
	serial.open()

	#Make stdin a non-blocking file
	fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)

	#Post startup message to other XBee's and a stdout
	serial.writelines("RPi #1 is up and running.\r\n")
	print "RPi #1 is up and running."

	switchColor(CMD_OUTPUT_TEXT)
	print "Entering loop to read and print messages (Ctrl-C to abort)..."

	#Main Loop
	try:
		while True:
			#Read a line from XBee and convert it from b'xxx\r\n' to xxx and print at stdout
			switchColor(TERM_OUTPUT_TEXT)
			line = serial.readline().decode('utf-8')
			if line:
				print line

			#Read data from keyboard (i.e. stdin) and send via the XBee modem
			switchColor(TERM_INPUT_TEXT)
			try:
				line = sys.stdin.readline()
				serial.writelines(line)
			except IOError:
				time.sleep(0.1)
				continue

	except KeyboardInterrupt:
		printc("\n*** Ctrl-C keyboard interrupt ***", ERROR_TEXT)
		serial.writelines("RPi #1 is going down . \r\n")

	finally:
		switchColor(CMD_INPUT_TEXT)
