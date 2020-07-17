#!/usr/bin/python
import logging
import hardwareManager
import serial
import threading
import time
import datetime

import pickledb
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
        self.readings = {}

        # Empty Database object
        self.database = None

        # Flags
        # add flags as nessissary (see identifyMessage())
        self.flags = {'resultReportingFlag' : True}

        logging.info("A OSMO 2020 Manager was created with SN: " + self.SN + " and Port: " + self.port)

    def assignDatabase(self, database):
        # Accepts a database for to use with this instument
        self.database = database

        # XXX: Need to check to see if these tables have already been created
        # XXX: Are the changes being made to the database here showing up in other places?

        # ----- Create OSMO key'd lists ----- #
        # Represents all the experiments that came from the OSMO manager that are unpaired
        self.database.lcreate('OsmoUnpairedTimestamp')
        # Represents all the keys that are sent from the HTTP Server
        self.database.lcreate('OsmoUnpairedSampleID')
        # Self explanitory, but *can* happen
        # Will be filled with sampleID's
        self.database.lcreate('OsmoUnsentLinkedData')

        self.database.dump()

        logging.debug("OSMO Manager Initilized database")


    def parseRecallData(self):
        # Return a dictionary of values
        # Parse data when we know we are receiving a 'Recall Data' message
        # We assume the header has already been read out of the input buffer to be identified (the hard part)
        # Trash a space
        self.readings.clear()

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

        # XXX: Gives an error in pylinter. readings is not an array
        self.readings.append({'IDNum':ID, 'reading':reading, 'date':date,'time':time})
        
        return self.readings

    def parseResultReportHeader(self):
        # Return a dictionary of values
        # Parse data when we know we are receiving a 'Result Reporting' message
        # We assume the header has already been read out of the input buffer to be identified (the hard part)
        self.readings = {}
        self.flags["resultReportingFlag"] = True
        # Clear some unneeded characters
        self.serialObj.read(13)

        # Begin parsing
        # Operator ID
        # Nb: If this field is unused, it will be a row of underscorees
        operatorID = self.serialObj.read(19)
        operatorID = operatorID.encode('ascii')

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

        self.serialObj.reset_input_buffer()
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
        ID = self.serialObj.read(3)
        #ID = ID.encode('ascii')
        #ID = int(ID)            # In the order they are listed in README
        
        self.readings[well] = {'IDNum':ID, 'measurement': measurement, 'well':well}

    def parseResultReportFooter(self):
        # Push it onto the stack
        # Clear the footer out of the input buffer
        self.serialObj.read(60)
        self.flags['resultReportingFlag'] = False

        measurementsByWell = []

        # Filtering out all the measurements
        for a in self.readings:
            if type(self.readings[a]) == dict:
                measurementsByWell.append(self.readings[a])


        # Adding the message to the stack
        self.stack.append(OsmoMessage(measurementsByWell,"mOsm/kg", "Result Report (Real Test)"))
        logging.debug("OSMO Manager finished parsing a 'Result Report' test and added it to the stack")

        # TODO: Rename this varible
        self.readings = {}

    def getInputBuffer(self):
        inputBufferSize = self.serialObj.in_waiting
        return inputBufferSize
    
    def parseHeaderRecallResults(self):
        # Assuming the first byte has been read 
        # We don't need 
        self.serialObj.read(18)

    def identifyMessage(self):
        # Checking input buffer to identify message, then pushing it onto the stack 
        # Check it three times
        parsedBufferRollingAverage = []
        # TODO: The number of times this is checked should be a member variable
        for i in range(0,3):
            # The size of the input buffer
            parsedBufferRollingAverage.append(self.getInputBuffer())
            # TODO: Sleep duration should be a member variable
            time.sleep(.25)

        # If we receaved the same reading
        # logging.debug("Received a rolling average of: " + str(parsedBufferRollingAverage))
        if all(parsedBufferRollingAverage):
            parsedBuffer = parsedBufferRollingAverage[0]
            logging.debug("OSMO2020Manager looping with a buffer of: " + str(parsedBuffer))
            # Checking flags
            # ========= FLAG CHECKING =========
            if(self.flags['resultReportingFlag'] == True):
                if(parsedBuffer == 15):
                    # Result
                    logging.debug("OSMO Manager identified a result command while the flag was set to true")
                    self.parseIndividualResult()
                    pass
                if(parsedBuffer == 60):
                    # Footer
                    logging.debug("OSMO Manager identified a footer command while the flag was set to true")
                    self.parseResultReportFooter()
            # ========= COMMANDS =========
            if(parsedBuffer == 19):
                # Recall Results or Probe bin tests
                # XXX: ASSUMING IT IS RECALL RESULTS FOR THE PURPOSES OF TESTING
                
                pass
            if(parsedBuffer == 111):
                # Result Reporting
                logging.debug("OSMO Manager identified a result reporting command")
                self.parseResultReportHeader()
                pass
            if(parsedBuffer == 15):
                # Statistics 
                logging.debug("OSMO Manager identified a statistics command")
                pass
            elif(parsedBuffer == 18):
                # Event Record
                pass
            elif(parsedBuffer == 37):
                # Assistance
                pass
            elif(parsedBuffer == 14):
                # A/D Tests
                pass
            elif(parsedBuffer == 18):
                # Solenoid test                
                pass
            elif(parsedBuffer == 24):
                # Display/Print Test
                pass
            elif(parsedBuffer == 26):
                # Key/Beeper Test
                pass
            elif(parsedBuffer == 26):
                # Barcode Test
                pass
            elif(parsedBuffer == 16):
                # Motor Test                
                pass
            elif(parsedBuffer == 26):
                # Select LIMS Out 
                pass
            elif(parsedBuffer == 14):
                # Exiting configuration
                pass

    def pop(self):
        # Is there an unpaired sample ID in the database
        # Yes: Pair the new data with the unpaired sample ID in the database
        # No:  Put an unpaired timestemp(representing unpaired data) in the database
        # XXX: (Assuming threading is put into the HTTP Server) 
        #       There is an unlikely chance that both the HTTP server and the manager write into the database at the same time

        if (self.stack == []):
            return

        logging.debug("OSMO has entered pop() method")

        # Hopefully this won't be confusing, removes and returns the first item in the manager's stack
        popedMessage = self.stack.pop(0)
        # The list representing the unpaired sample ID's is a FIFO stacktimestampPop
        unpairedSampleID = self.database.lgetall('OsmoUnpairedSampleID')

        if unpairedSampleID != []:
            # Get a string representing the new sample ID we are going to use
            sampleID = unpairedSampleID[0]

            self.database.dcreate(sampleID)
            self.database.dadd(sampleID, ('units',popedMessage.units))
            self.database.dadd(sampleID, ('label',popedMessage.label))
            # Unlikely the above two value will ever be referenced, but might help for diagnostics
            self.database.dadd(sampleID, ('timestampPop',datetime.datetime.now()))
            self.database.dadd(sampleID, ('timestampStack', popedMessage.timestampStack))
            
            for wellPair in popedMessage.value:
                # Should be a pair of (well,value)
                self.database.dadd(sampleID, ("Well#" + str(wellPair['well']), wellPair['measurement']))

            self.database.ladd('OsmoUnsentLinkedData', sampleID)
            # Write
            self.database.dump()


        # Doing elif for robsutness sake
        elif unpairedSampleID == []:
            # The portion of the code occurs if there is NO SampleID ready to be recieved
            timestamp = str(datetime.datetime.now())

            self.database.ladd('OsmoUnpairedTimestamp', timestamp)
            self.database.dcreate(timestamp)
            # Unlikely the above two value will ever be referenced, but might help for diagnostics
            self.database.dadd(timestamp, ('units',popedMessage.units))
            self.database.dadd(timestamp, ('label',popedMessage.label))

            self.database.dadd(timestamp, ('timestampPop',str(datetime.datetime.now())))
            self.database.dadd(timestamp, ('timestampStack', popedMessage.timestampStack))
            
            for wellPair in popedMessage.value:
                # Should be a pair of (well,value)
                self.database.dadd(timestamp, ("Well#" + str(wellPair['well']), wellPair['measurement']))

            # Write
            self.database.dump()

        # Save the database
        self.database.dump()

class OsmoMessage(object):
    def __init__ (self, value, units, label):
        # If the message is a reading, the measurment assoicated with it
        self.value = value
        # If the message is a reading, what units is it in?
        self.units = units
        # The label of the message (see README.md)
        self.label = label
        # Timestamp of object creation (When it was pushed onto the stack)
        self.timestampStack = str(datetime.datetime.now())# now
        # Timestamp of when it was poped from the stack
        
        logging.debug("Osmo message with a value of: " + str(self.value))
        logging.debug("Osmo message with a units of: " + self.units)
        logging.debug("Osmo message with a label of: " + self.label)
        logging.debug("Osmo message with a timestamp stack of " + str(self.timestampStack))