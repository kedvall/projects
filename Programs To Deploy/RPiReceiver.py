#! /usr/bin/python3
 
# imported modules
import os                   # portable way of using operating system dependent functionality
import sys                  # provides access to some variables used or maintained by the interpreter
import time                 # provides various time-related functions
import fcntl                # performs file control and I/O control on file descriptors
import serial               # encapsulates the access for the serial port
  
if __name__ == '__main__':

    serialConnection = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 112500,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
 
    # make stdin a non-blocking file
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
 
    # post startup message to other XBee's and at stdout
    serialConnection.write("RPi #1 is up and running.\r\n")
    print("RPi #1 is up and running.")
 
    print("Entering loop to read and print messages (Ctrl-C to abort)...")
 
    try:
        while True:
            # read a line from XBee and convert it from b'xxx\r\n' to xxx and print at stdout
            line = serialConnection.readline().decode('utf-8')
            if line:
                print(line)
 
            # read data from the keyboard (i.e. stdin) and send via the XBee modem
            try:
                line = sys.stdin.readline()
                serialConnection.write(line)
            except IOError:
                time.sleep(0.1)
                continue
 
    except KeyboardInterrupt:
        print("\n*** Ctrl-C keyboard interrupt ***")
        serialConnection.write("RPi #1 is going down.\r\n")