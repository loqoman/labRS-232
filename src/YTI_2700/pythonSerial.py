#!/usr/bin/python
# ----- Notes -----
'''
*.decode('ascii')
*.encode('ascii')
\r = carrage return
\r\n = CRLF
\ooo = ASCII character with octal value ooo
'''
import time
import serial

print("Current pySerial version: " + serial.__version__)    # Laptop is version 3.4
# configure the serial connections (the parameters differs on the device you are connecting to)
# some ports doo not support configurations 
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,       # Relevent to device
    stopbits=serial.STOPBITS_ONE,   # Relevent to device
    bytesize=serial.EIGHTBITS       # Relevent to device
)

ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            # Read size bytes from the serial port. If a timeout is set it may return less characters as requested. 
            # With no timeout it will block until the requested number of bytes is read.
            # Read one byte from serial
            out += ser.read(1)
            # input = ser.read(10) - read 10 bytes
            # input.encode/decode('ascii')

        if out != '':
            out.encode('ascii')
            print ">>" + out