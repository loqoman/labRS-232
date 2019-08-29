#!/usr/bin/python
import logging
import hardwareManager
import serial
import threading

# This is a trimmed down version of a basic Instument manager
# Nb: timeout for Serial object only affects the behaivor read()
# XXX: Communication holes
# TODO: Unit tests
# format(message.encode('hex')))

class OSMO2020Manager(object):

    def __init__(self, port, autoInit = False, SN, model):
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

        # TODO: Where auto-init functionality would be written in
        if autoInit:
            pass
        else:
            self.SN = SN
            self.model = model

        # Clear anything that may have been in the input buffer
        self.serialObj.reset_input_buffer()

        logging.info("A OSMO 2020 Manager was created with SN: " + self.SN + " and Port: " + self.port)

    def parseRecallData(self):
        # Reads the data in the proper known format
        # This method assumes that the next 67 bytes of the input buffer are a 'recall data' message 
        
        pass

    def parseResultReportData(self):
        # Reads data from serial input buffer
        # This method assumes that the next 15 bytes of the input buffer are a 'recall data' message 
        # Gives you ASCII: <space><well(ex:1)>:
        well = self.serialObj.read(3) 
        well = well.encode('ascii')

        # Gives you ASCII: <space><space><measurement(ex: 293)>
        measurment = self.serialObj.read(5) 
        measurment = measurment.encode('ascii')

        # TODO: The 'measurement' field here is untested, when the hex dump was
        #       recorded, the field was empty. I *think* this byte-pattern is correct.
        # Gives you ASCII <space><'I'><'D'><':'><ID>
        ID = ser.read(5)
        ID = ID.encode('ascii')
        
        # TODO: Convert well, ID, and measurement into int objects
        return {'wellNum': well, 'measurement': measurment, 'IDNum': ID}

    def blockForInput(self, byteTimeout = 100):
        logging.warning("Osmo manager with SN " + SN + " is blocking waiting for " + str(byteTimeout) + "bytes.")
        # By deafult wait for 100 bytes

    def blockSelfIdentify(self):
        logging.warning("An osmo manager is blocking, waiting for self-initialization")
        pass
    
    def identifyMessage(self, message):
        # Method to block and wait for a command, then self-identify
        pass