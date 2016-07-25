#! python3
 
# imported modules
import os                   # portable way of using operating system dependent functionality
import sys                  # provides access to some variables used or maintained by the interpreter
import time                 # provides various time-related functions
import fcntl                # performs file control and I/O control on file descriptors
import serial               # encapsulates the access for the serial port
from pretty import switchColor, printc  # provides colored text for xterm & VT100 type terminals using ANSI escape sequences
 
# text colors to be used during terminal sessions
ERROR_TEXT = 'bright red'
CMD_INPUT_TEXT = 'normal'
CMD_OUTPUT_TEXT = 'bright yellow'
TERM_OUTPUT_TEXT = 'purple'
TERM_INPUT_TEXT = 'bright purple'
 
if __name__ == '__main__':
    serial = serial.Serial()
    serial.port = '/dev/ttyUSB0'
    serial.baudrate = 112500
    serial.timeout = 1
    serial.writeTimeout = 1
    serial.open()
 
    # make stdin a non-blocking file
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
 
    # post startup message to other XBee's and at stdout
    serial.writelines("RPi #1 is up and running.\r\n")
    print("RPi #1 is up and running.")
 
    switchColor(CMD_OUTPUT_TEXT)
    print("Entering loop to read and print messages (Ctrl-C to abort)...")
 
    try:
        while True:
            # read a line from XBee and convert it from b'xxx\r\n' to xxx and print at stdout
            switchColor(TERM_OUTPUT_TEXT)
            line = serial.readline().decode('utf-8')
            if line:
                print(line)
 
            # read data from the keyboard (i.e. stdin) and send via the XBee modem
            switchColor(TERM_INPUT_TEXT)
            try:
                line = sys.stdin.readline()
                serial.writelines(line)
            except IOError:
                time.sleep(0.1)
                continue
 
    except KeyboardInterrupt:
        printc("\n*** Ctrl-C keyboard interrupt ***", ERROR_TEXT)
        serial.writelines("RPi #1 is going down.\r\n")
 
    finally:
        switchColor(CMD_INPUT_TEXT)