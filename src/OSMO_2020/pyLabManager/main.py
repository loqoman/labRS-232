from hardwareManager import HardwareManager
from OSMO2020Manager import OSMO2020Manager
import result
import logging
import parser

# If This exact file is running
if __name__ = "__main__":
    ''' 
    Psudocode

    myResult = Result(units = 'in', value = 1)

    wantedInsturment = myHardwareManager.getInstumentByModel(someKnownModel)

    hardwareManager.assoicateResultWithInsturment(resultObject, hardwareManager, method, value)
    