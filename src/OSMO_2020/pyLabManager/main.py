from hardwareManager import HardwareManager
from OSMO2020Manager import OSMO2020Manager
from result import Result 
import parser,time,sys, logging
# Slight abstraction over the normal http library
import httpServer 

# Database Imports
import pickledb

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)-6s: %(message)s",
                    datefmt="%m/%d %H:%M:%S",
                    filename="logs/pyLabLogs.log",
                    filemode="a")

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logging.info("*------* Started main.py *------* ")

# If This exact file is running
if __name__ == "__main__":
    # Creating Database
    database = pickledb.load('OsmoDB.db', False)
    database.dump()

    httpServer.registerDatabase(database)
    # Create the HTTP Server
    osmoHTTP = httpServer.labManagerHTTPServer(port=8080,ip='localhost',handler=httpServer.osmoHandler)
    #osmoHTTP.assignDatabase(database)
    # Small confusion between begin() and run() in the http server
    # Spins off a thread that the HTTP server runs in
    osmoHTTP.begin()

    # Create the hardware Manager
    masterHardwareManager = HardwareManager()
    # TODO: In the future, I think having a specific member variable to keep track of an instument-specific manager would be good
    masterHardwareManager.registerDatabase(database)

    # Create the Osmo2020 Manager
    testOsmo = OSMO2020Manager(port = "/dev/ttyUSB0",
                               SN = "05030326A", 
                               model = "OMSO_2020") 

    # Register the Omos manager
    masterHardwareManager.registerInsturmentManager(testOsmo)

    # Let settle
    time.sleep(2)

    # Starting main loop
    masterHardwareManager.loop()

