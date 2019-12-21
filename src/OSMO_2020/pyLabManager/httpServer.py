from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import threading, logging 
import pickledb
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
# This class will handles any incoming request from
# the browser 

globalDatabase = None


def registerDatabase(Database):
    global globalDatabase
    globalDatabase = Database

class insturmentHandler(BaseHTTPRequestHandler):
	

    def do_GETDIAGNOSTICS(self):
        # Levaing empty for now; Something that might come in handy later
        pass 

    def do_OSMO2020COMMAND(self):
        # Psudocode
        logging.debug("Recieved an OSMO 2020 command from a client, prepairing data...")

        # TODO: What is the terminology of this *specific* http request part 
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data

        # TODO: MAKE SURE THE SENT DATA IS **ONLY** A SAMPLE ID. NOTHING ELSE
        # XXX: What if this is empty?
        sampleID = self.rfile.read(content_length) # <--- Gets the data itself


        # If there is an unpaired timestamp, needs to be paired
        # If there is no unpaired timestamp, put the sampleID in the Database
        unpairedTimestampList = globalDatabase.lgetall('OsmoUnpairedTimestamp')
        unsentData = globalDatabase.lgetall('OsmoUnsentLinkedData')

        if unsentData != []:

            returnStatusHeader = 'Found unsent linked data, sending instead of the passed sampleID. Please send again.'

            globalDatabase.lpop('OsmoUnsentLinkedData',0)
            unsentKey = unsentData[0]

            returnString = 'Sample ID of: ' + unsentKey + 'With Well Values: '
            sampleIDKeys = globalDatabase.dkeys(unsentKey)

            for key in sampleIDKeys:
                if 'Well#' in key:
                    returnString += key + ': '
                    returnString += globalDatabase.dget(unsentKey, key)
                    returnString += '  |  '

            # Write
            globalDatabase.dump()

        # If there IS an unpaired timestamp
        elif unpairedTimestampList != []:
            # We need to get all the keys, and all the values to move into a new dict
            # Get the oldest unpaired timestamp
            # Used when sending HTTP response
            returnStatusHeader = 'Paired with an unpaired result in the Database and sending'

            timestampDict = unpairedTimestampList[0]
            globalDatabase.lpop('OsmoUnpairedTimestamp', 0)

            # List of all keys in the timestamp entry
            keysToMove = globalDatabase.dkeys(timestampDict)
            # List of all values in the timestamp entry
            valuesToMove = globalDatabase.dvals(timestampDict)

            globalDatabase.dcreate(sampleID)

            # This code snippit should move all the key values into a new Database entry
            index = 0
            for key in keysToMove:
                globalDatabase.dadd(sampleID, (key,valuesToMove[index]))
                index += 1

            # Write
            globalDatabase.dump()

            returnString = 'Sample ID of: ' + sampleID + 'Well Values: '
            sampleIDKeys = globalDatabase.dkeys(sampleID)

            for key in sampleIDKeys:
                if 'Well#' in key:
                    returnString += key + ': '
                    returnString += globalDatabase.dget(sampleID, key)
                    returnString += '  |  '

        # elif for robustness
        elif unpairedTimestampList == []:
            # The event where no data is ready for processing
            # XXX: THERE is a course of events where the the data is paired by the OMSO manager,
            #       then not sent by the HTTP server.
            globalDatabase.ladd('OsmoUnpairedSampleID', sampleID)

            returnStatusHeader = 'Added the sample ID to the queue of unpaired sampleIDs'

            # TODO: needs to be double checked
            returnString = 'Waiting on the following sample IDs to be paired: '

            returnString += globalDatabase.lgetall('OsmoUnpairedSampleID')

        self.send_response(200)
        # Standard HTTP patterns 
        self.send_header('Content-type', 'text')
        self.send_header('Status', returnStatusHeader)
        self.end_headers()

        logging.debug("Returning data to a client with the status of: " + returnStatusHeader)


        # TODO: This has to be enumerated with Chris, what we want to send. 
        #       For now, stich all the well values together and send it over
        # Eventially, returnstring should be a little formatted string of all the well values found for a result
        globalDatabase.dump()
        self.wfile.write(returnString)
            
class labManagerHTTPServer(threading.Thread):
    def __init__(self, port, ip, handler):
        # Threading-Specific Stuff
        threading.Thread.__init__(self)
        self.daemon = True
        # HTTP-Specific object variables
        self.port = port
        
        # TODO: Make this a passed argument
        self.handler = handler
        self.server = HTTPServer((ip, port), self.handler)

        # OSMO specific Database
        # XXX: Need more member variables to represent different Databases

    def begin(self): 
        self.start()

    def run(self):
        self.server.serve_forever()

