#!/usr/bin/python
import serial
import logging
import time
import sys
# Create Serial moule 
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,       # Relevent to device
    stopbits=serial.STOPBITS_ONE,   # Relevent to device
    bytesize=serial.EIGHTBITS       # Relevent to device
)


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-6s: %(message)s",
                    datefmt="%m/%d %H:%M:%S",
                    filename="serialLogs.log",
                    filemode="a")

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logging.info("*------* Started serialBlocking.py *------* ")
# Main loop


def parseRecallData(inBufSize):
    # Add assert messsage here
    # assert inBufSize = 67

    # Read the first 5 bytes, which are the ID
    ID = ser.read(5)

    # Read the next 7 bytes, which are the measurement value
    measurment = ser.read(7)

    # Read the next 5 bytes, which are the units
    units = ser.read(4)
   
    # Get them out of the input buffer
    ser.reset_input_buffer()
    return ID, measurment, units

def parseResultReportData(inBufSize):
    # Add assert messsage here
    # assert inBufSize = 15

    # Read the first 5 bytes, which are the ID
    well = ser.read(3)

    measurment = ser.read(5)
    
    ID = ser.read(4)

    # Get them out of the input buffer
    ser.reset_input_buffer()
    return ID, measurment

def parseSpew(inBufSize):
    # Add assert messsage here

    message = ser.read(inBufSize)

    # Clear input buffer
    # ser.reset_input_buffer()
    return message

while True:
    # Sleep
    time.sleep(2)
    # Clear the output string
    out = ''

    # If there is things in the output buffesr
    if ser.inWaiting() > 0:
        
        logging.info("Recieved an input buffer of {}".format(ser.inWaiting()))

        message = parseSpew(ser.in_waiting)
        '''
        ID,measurment, units = parseRecallData(ser.inWaiting())
        logging.info("Parsed an ID of: {}".format(ID))
        logging.info("Parsed a measurment of: {}".format(measurment))
        logging.info("Parsed a units of: {}".format(units))
        '''
        logging.info("Parsed a message(hex) of: {}".format(message.encode('hex')))
        logging.info("Parsed a message(normal) of: {}".format(message))


