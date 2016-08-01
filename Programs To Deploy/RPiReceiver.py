#! /usr/bin/python3
 
# imported modules
import os                   # portable way of using operating system dependent functionality
import sys                  # provides access to some variables used or maintained by the interpreter
import time                 # provides various time-related functions
import fcntl                # performs file control and I/O control on file descriptors
import serial               # encapsulates the access for the serial port
  
if __name__ == '__main__':

    try:
        serialConnection = serial.Serial(
            "/dev/ttyUSB0", # Use ttyAMA0 for GPIO
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            writeTimeout = 0,
            timeout = 10,
            rtscts=False,
            dsrdtr=False,
            xonxoff=False)
    except serial.SerialException:
        print('Could not find /dev/ttyUSB0. Are you sure XBee is plugged in?')
        print('Exiting...')
        sys.exit()
 
    # make stdin a non-blocking file
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
 
    # post startup message to other XBee's and at stdout
    print("Receiver1 is up and running.")
    print("Entering loop to read and print messages (Ctrl-C to exit)...")
 
    try:
        while True:
            # read a line from XBee and convert it from b'xxx\r\n' to xxx and print at stdout
            try:
                line = serialConnection.readline().decode('utf-8')
            except UnicodeDecodeError:
                print('*** Invalid Character in Data Stream ***')
            if line:
                print(line, end='')

    except KeyboardInterrupt:
        print("\n*** Keyboard Interrupt - Exiting... ***")