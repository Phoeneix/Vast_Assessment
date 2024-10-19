'''Starter of the Test Execution'''
import sys
import pytest
import datetime

from config.global_constants import GlobalConstants

if __name__ == '__main__':
    '''
    The main executor
    '''

    # Setting global constants
    GlobalConstants.OPERATION_LENGTH = 4320
    GlobalConstants.CURRENT_TIME = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Executing test cases
    exit_code = pytest.main(['-s'])
    if exit_code == 0:
        print('All tests passed!')
    else:
        print('Some tests failed.')
        print(f'Exit_code: "{exit_code}"')
        sys.exit(exit_code)

