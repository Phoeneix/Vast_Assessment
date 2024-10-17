'''Starter of the Program'''

import argparse
import sys

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

    parser.add_argument('-l',
                        help='The length of the operation in minutes',
                        required=False,
                        default=4320,
                        type=int)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    '''
    The main executor
    '''

    args = ParseArguments()
    print(args)

    operation = MiningOperation(
        mining_truck_count = args.n,
        mining_station_count = args.m,
        operation_length = args.l)

    operation.FlowOrganizer()
