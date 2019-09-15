#!/usr/bin/python

import datetime

# NOTE: Right now, this is bare bones. Proper Object-orientation practices have not been implemented with the hardwareManager
#       or any insturment manager. In the future, the hand-off will be much more gracefull.
class Result(object):
    
    # -1 because 0 is valid for most of these feilds
    def __init__(self, units, value = -1, ID = -1, well = -1):
        # String representing what the values mean
        self.units = ''
        self.value = value 
        self.ID = ID

        self.well = well
        # Timestamps
        # Time at which *THE OBJECT* was created
        self.creationTimestamp = datetime.datetime.now()
        self.requestTimestamp = 0

        self.hardwareManager = 0
    
    # More to come?