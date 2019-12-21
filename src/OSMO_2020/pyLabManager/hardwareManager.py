#!/usr/bin/python
import logging
hardwareManager = None

class HardwareManager(object):

    # Called when a hardware manager is created
    def __init__(self):
        # Singleton Logic
        global hardwareManager

        # ----- Prepping Lists ----- 
        # List of intumentManager objects
        self.insturmentManagers = []

        # These lists exist to provide better logging feedback about known / unknown inturments.
        # The functionallity of keeping track of known / unknown SN's and models has the potential to
        # Be a renowed feature in the future, namely with further user-facing elements.
        # (For example, configurations specifing which insturments to register on start-up)
        # For now, these lists are strings.
        self.knownSerialNumbers = []
        self.knownModels = []

        # Init empty database
        self.database = None
        
        # Assigning the single hardwareManager
        if hardwareManager is None:
            logging.info("Creating a new global hardwareManager")
            hardwareManager = self
        else:
            logging.warning("Overriding the old hardwareManager")
            hardwareManager = self

    # Find all insturments matching a model(OMSO_2020, ect.)
    # Model is a string
    def listInsturmentsByModel(self, model = ''):
        returnedList = []

        # TODO: model input checking
        for insturment in self.insturmentManagers:
            if insturment.model == model:
                returnedList.append(insturment)

    # Find all insturments matching a serial number(ex: 05030326A)
    # Serial number is a string
    def listInsturmentsBySN(self, SN = ''):
        returnedList = []

        for insturment in self.insturmentManagers:
            if insturment.SN == SN:
                returnedList.append(insturment)

    def registerDatabase(self, database):
        # Acceps a passed database
        # On register on an insturmentManager, assigns the database to that insturment manager
        self.database = database

    # Returns bool representing the success of the register
    def registerInsturmentManager(self, insturmentManager):
        
        insturmentSN = insturmentManager.SN
        insturmentModel = insturmentManager.model

        # TODO: Wire both of these in with configs.
        #       (Whenever an unknown insturment is registered, write it to a file, and populate the known* lists)
        #       (With the file contents)
        if insturmentModel not in self.knownModels:
            logging.info("Attempting to register an insturment with an unknown model")

            # Safty measures, to prevent unwanted access to a new (potentially expensive) device.
            # Human language!
            while True:
                continueStr = raw_input("Proceed? (Y/N)")

                logging.debug("Passed an input of: " + continueStr)
                if continueStr == 'Y':
                    # Get out of the loop
                    break

                elif continueStr == 'N':
                    logging.info("Exiting register method")
                    # Break out of full method
                    return False
                else:
                    logging.info("Unrecgognised Input, Please type 'Y' or 'N'")

            logging.warning("Registering an unknown model of: " + insturmentModel)
            self.knownModels.append(insturmentModel)

        if insturmentSN not in self.knownSerialNumbers:
            logging.info("Attempting to register an insturment with an unknown Serial number")
            # Safty measures, to prevent unwanted access to a new (potentially expensive) device.
            # Human language!
            while True:
                continueStr = raw_input("Proceed? (Y/N)")

                logging.debug("Passed an input of: " + continueStr)
                if continueStr == 'Y':
                    # Get out of the loop
                    break

                elif continueStr == 'N':
                    logging.info("Exiting register method")
                    # Break out of full method
                    return False
                else:
                    logging.info("Unrecgognised Input, Please type 'Y' or 'N'")

            logging.warning("Registering an unknown SN of: " + insturmentSN)
            self.knownSerialNumbers.append(insturmentSN)

        # Appending the object
        # XXX: Come back and double-check this later, should be fine for now
        if (self.database is not None):
            insturmentManager.assignDatabase(self.database)
            
        self.insturmentManagers.append(insturmentManager)
        

    def loop(self):
        # ===== Main Loop =====
        while True:
            for manager in self.insturmentManagers:
                manager.identifyMessage()
                #manager.pop()

    
        
    