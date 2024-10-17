'''The file for the test cases'''

from mining_operation import MiningOperation

# Constants
OPERATION_LENGTH = 4320

def test_negative_0_trucks():
    '''Negative Test case to test of 0 trucks input'''

    print('\n\n\n====================================== test_negative_0_trucks ==================================================')
    try:
        operation = MiningOperation(
            mining_truck_count = 0,
            mining_station_count = 1,
            operation_length = OPERATION_LENGTH).FlowOrganizer()
    except AssertionError as e:
        print(e.args)


def test_negative_0_station():
    '''Negative Test case to test of 0 stations input'''

    print('\n\n\n====================================== test_negative_0_station ==================================================')
    try:
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 0,
            operation_length = OPERATION_LENGTH).FlowOrganizer()
    except AssertionError as e:
        print(e.args)


def test_negative_0_operation_length():
    '''Negative Test case to test of 0 operation length input'''

    print('\n\n\n====================================== test_negative_0_operation_length ==================================================')
    try:
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 1,
            operation_length = 0).FlowOrganizer()
    except AssertionError as e:
        print(e.args)


def test_positive_10_trucks_10_stations():
    '''Test case to test behavior with 10 trucks and 10 stations
       Intended to test normal behavior'''

    print('\n\n\n====================================== test_positive_10_trucks_10_stations ==================================================')
    result = MiningOperation(
        mining_truck_count = 10,
        mining_station_count = 10,
        operation_length = OPERATION_LENGTH).FlowOrganizer()
    assert result, 'Test failed to finish as intended!'


def test_positive_5000_trucks_10_stations():
    '''Test case to test behavior with 5000 trucks and 10 stations
       Intended to test load balancing and wait time handling behavior and the stopping when wait times
       extends above operation length'''

    print('\n\n\n====================================== test_positive_1000_trucks_1_stations ==================================================')
    result = MiningOperation(
        mining_truck_count = 5000,
        mining_station_count = 10,
        operation_length = OPERATION_LENGTH).FlowOrganizer()
    assert result, 'Test failed to finish as intended!'