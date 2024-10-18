'''Starter of the Test Execution'''
import sys
import pytest


if __name__ == '__main__':
    '''
    The main executor
    '''

    exit_code = pytest.main(['-s'])
    if exit_code == 0:
        print('All tests passed!')
    else:
        print('Some tests failed.')
        print(f'Exit_code: "{exit_code}"')
        sys.exit(exit_code)

