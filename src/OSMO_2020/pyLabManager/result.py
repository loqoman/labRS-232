import datetime

class Result(object):
    
    def __init__(self, units, value = 0, hardwareManager):
        # String representing what the values mean
        self.units = 0
        self.value = 0 

        # Time at which *THE OBJECT* was created
        self.creationTimestamp = datetime.datetime.now()
        self.requestTimestamp = 0

        self.hardwareManager = 0
    
        if
