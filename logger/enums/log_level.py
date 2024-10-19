'''The log level enum'''

from enum import Enum
from pickle import NONE


class LogLevel(Enum):
    '''The log level enum'''

    NONE = 0
    INFO = 1
    DEBUG = 2


    def FromStr(value:str):
        '''Method to convert the string to the enum'''

        if value.lower() in ['none', 'null', 'n/a', '']:
            return LogLevel.NONE
        elif value.lower() in ['info']:
            return LogLevel.INFO
        elif value.lower() in ['debug']:
            return LogLevel.DEBUG
        else:
            raise NotImplementedError(f'Handling for "{value}" is not implemented!')
