from hardwareManager import HardwareManager
from OSMO2020Manager import OSMO2020Manager
from result import Result
import logging
import parser
import time
import sys

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-6s: %(message)s",
                    datefmt="%m/%d %H:%M:%S",
                    filename="logs/pyLabLogs.log",
                    filemode="a")

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logging.info("*------* Started main.py *------* ")

# If This exact file is running
if __name__ == "__main__":
    # Create the test result
    # testResult = Result(units = 'milliOsmo', value = None)
    
    # Create the hardware Manager
    masterHardwareManager = HardwareManager()

    # Create the Osmo2020 Manager
    testOsmo = OSMO2020Manager(port = "/dev/ttyUSB0",
                               SN = "05030326A", 
                               model = "OMSO_2020") 

    # Register the Omos manager
    masterHardwareManager.registerInsturmentManager(testOsmo)

    # Let settle
    time.sleep(5)

    # Starting main loop
    masterHardwareManager.loop()

'''

        while (True):
        continueStr = raw_input("Ready to take measurement? (Y/N)")

        logging.debug("Passed an input of: " + continueStr)
        if continueStr == 'Y':
            # Get out of the loop
            break

        elif continueStr == 'N':
            logging.notice("Exiting...")
            # Break out of full method
            break
        else:
            logging.info("Unrecgognised Input, Please type 'Y' or 'N'")

    testResult = testOsmo.parseResultReportData()

    logging.info("Printing some facts about the result object returned")
    logging.info("Value: " + str(testResult.value))
    logging.info("Units: " + str(testResult.units))
    logging.info("Well: " + str(testResult.well))
    logging.info("ID: " + str(testResult.ID))

'''
            
