#!/usr/bin/python
import logging
import hardwareManager
import serial
import threading
import time
import datetime

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
        
        # Initilizing the stack
        self.stack = []

        # Flags
        # add flags as nessissary (see identifyMessage())
        self.flags = {'resultReportingFlag' = False}

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

        readings.append({'IDNum':ID, 'reading':reading, 'date':date,'time':time})
        
        return readings

    def parseResultReportHeader(self):
        # Return a dictionary of values
        # Parse data when we know we are receiving a 'Result Reporting' message
        # We assume the header has already been read out of the input buffer to be identified (the hard part)
        self.readings = {}}
        self.flags["resultReportingFlag"] = True
        # Clear some unneeded characters
        self.serialObj.read(13)

        # Begin parsing
        # Operator ID
        # Nb: If this field is unused, it will be a row of underscorees
        operatorID = self.serialObj.read(19)
        operatorID = operatorID.encode('ascii'))

        # Clear some unneeded characters
        self.serialObj.read(5)

        serialNumber = self.serialObj.read(9)
        serialNumber = serialNumber.encode('ascii')

        # Clear some unneeded characters
        self.serialObj.read(1)

        date = self.serialObj.read(10)
        date = date.encode('ascii')

        # Clear some unneeded characters
        self.serialObj.read(1)

        time = self.serialObj.read(11)
        time = time.encode('ascii')

        # The 'readings' object acts as an intermediate buffer between the object going onto the stack, and multiple funciton
        self.readings["operatorID"] = operatorID
        self.readings["serialNumber"] = serialNumber
        self.readings["date"] = date
        self.readings["time"] = time

    def parseIndividualResult(self):

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
        ID = int(ID)            # In the order they are listed in README
        
        self.readings[well] = {'IDNum':ID, 'measurement': measurement, 'well':well}

    def parseResultReportFooter(self):
        # Push it onto the stack
        # Clear the footer out of the input buffer
        self.serialObj.read(60)
        self.flags['resultReportingFlag'] = False

        measurementsByWell = []

        # Filtering out all the measurements
        for a in self.readings:
            if type(self.readings[a]) = dict:
                measurementsByWell.append(self.readings[a])


        self.stack.append(OsmoMessage(measurementsByWell,"mOsm/kg", "Result Report (Real Test)", (self.readings["date"],self.readings["time"]) )

    def getInputBuffer(self):
        inputBufferSize = self.serialObj.in_waiting()
        return inputBufferSize
    
    def indentifyMessage(self):
        # Checking input buffer to identify message, then pushing it onto the stack 
        # Check it three times
        parsedBufferRollingAverage = []
        # TODO: The number of times this is checked should be a member variable
        for i in range(0,3):
            # The size of the input buffer
            parsedBuffer.append(self.getInputBuffer)
            # TODO: Sleep duration should be a member variable
            time.sleep(.2)

        # If we receaved the same reading
        if all(parsedBuffer):
            parsedBuffer = parsedBuffer[0]
            # Checking flags
            # ========= FLAG CHECKING =========
            if(self.flags['resultReportingFlag'] = True):
                if(parsedBuffer = 15):
                    # Result
                    self.parseIndividualResult()
                if(parsedBuffer = 60):
                    # Footer
                    self.parseResultReportFooter()
            # ========= COMMANDS =========
            if(parsedBuffer = 19):
                # Recall Results
                pass
            if(parsedBuffer = 111):
                # Result Reporting
                logging.debug("OSMO Manager identified a result reporting command")
                self.parseResultReportHeader()
                pass
            if(parsedBuffer = 15):
                # Statistics 
                pass
            elif(parsedBuffer = 18):
                # Event Record
                pass
            elif(parsedBuffer = 37):
                # Assistance
                pass
            elif(parsedBuffer = 14):
                # A/D Tests
                pass
            elif(parsedBuffer = 19):
                # Probe Bin Tests
                pass
            elif(parsedBuffer = 18):
                # Solenoid test                
                pass
            elif(parsedBuffer = 24):
                # Display/Print Test
                pass
            elif(parsedBuffer = 26):
                # Key/Beeper Test
                pass
            elif(parsedBuffer = 26):
                # Barcode Test
                pass
            elif(parsedBuffer = 16):
                # Motor Test                
                pass
            elif(parsedBuffer = 26):
                # Select LIMS Out 
                pass
            elif(parsedBuffer = 14):
                # Exiting configuration
                pass
            elif():         
class OsmoMessage(object):
    def __init__ (value, units, label, timestampStack, timestampPop):
        # If the message is a reading, the measurment assoicated with it
        self.value = value
        # If the message is a reading, what units is it in?
        self.units = units
        # The label of the message (see README.md)
        self.label = label
        # Timestamp of object creation (When it was pushed onto the stack)
        self.timestampStack = # now
        # Timestamp of when it was poped from the stack
        self.timestampPop = None
        # self.sizeBytes
        

        # XXX: PROBLEM WITH MID MESSAGE
        #   We don't know how many wells are going to be done in this single command.
        #   we know when we are done, because we will receieve a footer.
        #   RIGHT HERE in software is where the logic to identify the next command's size is going to be.
        #   If the size = 15, do another reading
        #   If the size = 60, stop the reading and return all the messages