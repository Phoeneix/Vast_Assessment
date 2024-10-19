'''Starter of the Program'''

import argparse
import sys
import datetime

from config.global_constants import GlobalConstants
from mining_operation import MiningOperation


def ParseArguments():
    '''
    Parses the program arguments
    Returns
    -------
    args
    '''

    parser = argparse.ArgumentParser(
        description='Collect data from repositories and put it in a spreadsheet',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-n',
                        help='The count of mining trucks',
                        required=True,
                        type=int)

    parser.add_argument('-m',
                        help='The count of mining stations',
                        required=True,
                        type=int)

    parser.add_argument('-o',
                        help='The length of the operation in minutes',
                        required=False,
                        default=4320,
                        type=int)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    '''The main executor'''

    args = ParseArguments()

    # Setting global constants
    GlobalConstants.OPERATION_LENGTH = args.o
    GlobalConstants.CURRENT_TIME = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    operation = MiningOperation(
        mining_truck_count = args.n,
        mining_station_count = args.m)

    operation.StartOperation()
