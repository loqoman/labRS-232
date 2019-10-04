#!/usr/bin/python
import logging
import hardwareManager
import serial
import threading
import time

import result

# This is a trimmed down version of a basic Instument manager
# Nb: timeout for Serial object only affects the behaivor read()
# XXX: Communication holes
# TODO: Unit tests
# format(message.encode('hex')))

class OSMO2020Manager(object):

    def __init__(self, port, autoInit = False, SN = 0 , model = None):
        # XXX: Assert baud is 9600
        # Creating memeber varibles
        self.port = port
        self.autoInit = autoInit
        # Subject to change
        self.model = model

        self.serialObj = serial.Serial(
            port= self.port,
            baudrate= 9600,
            parity=serial.PARITY_NONE,      # Specific to 2020
            stopbits=serial.STOPBITS_ONE,   # ^
            bytesize=serial.EIGHTBITS       # ^
        )


        self.SN = SN
        self.model = model

        # Clear anything that may have been in the input buffer
        self.serialObj.reset_input_buffer()

        logging.info("A OSMO 2020 Manager was created with SN: " + self.SN + " and Port: " + self.port)

    def parseRecallData(self):
        # Return a dictionary of values
        # Parse data when we know we are receiving a 'Recall Data' message
        # We assume the header has already been read out of the input buffer to be identified (the hard part)
        # Trash a space
        readings = []

        # TODO: Double check this header size is correct
        self.serialObj.read(116)

        # Assuming a result is in the input buffer
        # This could also be sanity checked to make sure it is 65 bytes wide
        self.serialObj.read(2)

        ID = self.serialObj.read(3)
        ID = int(ID.encode('ascii'))

        self.serialObj.read(2)
        reading = self.serialObj.read(3)
        reading = int(reading.encode('ascii'))

        self.serialObj.read(30)
        date = self.serialObj.read(10)
        # At the end of the day, the date will always be read by a human. No need to int()
        date = date.encode('ascii')

        self.serialObj.read(1)
        time = self.serialObj.read(11)
        time = time.encode('ascii')

        # XXX: PROBLEM WITH MID MESSAGE
        #   We don't know how many wells are going to be done in this single command.
        #   we know when we are done, because we will receieve a footer.
        #   RIGHT HERE in software is where the logic to identify the next command's size is going to be.
        #   If the size = 65, do another reading
        #   If we don't get another message in the input buffer, assume we have exited

        readings.append({'IDNum':ID, 'reading':reading, 'date':date,'time':time})
        
        return readings
    def parseResultReportData(self):
        # Return a dictionary of values
        # Parse data when we know we are receiving a 'Result Reporting' message
        # We assume the header has already been read out of the input buffer to be identified (the hard part)
        readings = []
        # Trash a space
        self.serialObj.read(1)

        well = self.serialObj.read(1)
        well = well.encode('ascii')
        well = int(well)
        # Trash some junk in the message
        self.serialObj.read(3)

        # Get the measurement
        measurement = self.serialObj.read(3)
        measurement = measurement.encode('ascii')
        measurement = int(measurement)

        self.serialObj.read(4)
        # TODO: What happens if an ID is supplied? Where is it put?
        ID = self.serialObj.read(1)
        ID = ID.encode('ascii')
        ID = int(ID)

        # XXX: PROBLEM WITH MID MESSAGE
        #   We don't know how many wells are going to be done in this single command.
        #   we know when we are done, because we will receieve a footer.
        #   RIGHT HERE in software is where the logic to identify the next command's size is going to be.
        #   If the size = 15, do another reading
        #   If the size = 60, stop the reading and return all the messages

        readings.append({'IDNum':ID, 'measurement':measurement, 'well':well})
        return readings

    def blockForInput(self, byteTimeout = 100):
        logging.notice("Osmo manager with SN " + SN + " is blocking waiting for " + str(byteTimeout) + "bytes.")
        # By deafult wait for 100 bytes
        while self.getInputBuffer() < byteTimeout:
            logging.warning("Waiting for input...")
            time.sleep(5)
            
        out = self.serialObj.read(byteTimeout)
        return out

    def getInputBuffer(self):
        inputBufferSize = self.serialObj.in_waiting()

        return inputBufferSize
    
    def identifyMessage(self, message):
        # Method to block and wait for a command, then self-identify
        pass
        
        
        