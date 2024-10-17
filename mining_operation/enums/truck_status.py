from enum import Enum

class TruckStatus(Enum):
    '''The truck status enum'''

    MINING = 0
    TRAVELING_TO_STATION = 1
    WAITING_AT_STATION = 2
    UNLOADING = 3
    TRAVELING_TO_SITE = 4