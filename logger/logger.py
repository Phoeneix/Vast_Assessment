'''The logger file'''

from config.global_constants import GlobalConstants
from utils.file_handler import FileHandler


class Logger():
    '''The logger class'''

    def Log(value:str):
        '''Method to log text both into stdout and into a file'''

        print(value)
        FileHandler.SaveIntoFile(
            content = value,
            file_name = GlobalConstants.LOG_FILE)

        # Return the value for the exceptions / errors to be able to throw the text
        return value
