'''The file for the test cases'''
from sys import maxsize

from config.global_constants import GlobalConstants
from logger.logger import Logger
from mining_operation import MiningOperation


def test_negative_0_trucks():
    '''Negative Test case to test of 0 trucks input'''

    print('\n\n\n=================================== test_negative_0_trucks =============================================================')
    error_message = ''
    expected_message = 'One of the key information is missing to start the operation!\nMining Truck Count = 0\nMining Stations Count = 1\nOperation length = 4320'
    try:
        operation = MiningOperation(
            mining_truck_count = 0,
            mining_station_count = 1).StartOperation()
    except AssertionError as e:
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_trucks_negative_value():
    '''Negative Test case to test of -1 trucks input'''

    print('\n\n\n=================================== test_negative_trucks_negative_value ================================================')
    error_message = ''
    expected_message = 'One of the key information is missing to start the operation!\nMining Truck Count = 0\nMining Stations Count = 1\nOperation length = 4320'
    try:
        MiningOperation(
            mining_truck_count = -1,
            mining_station_count = 1).StartOperation()
    except AssertionError as e:
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_trucks_input_type():
    '''Negative Test case to test trucks input type'''

    print('\n\n\n=================================== test_negative_trucks_input_type ====================================================')
    error_message = ''
    expected_message = "'str' object cannot be interpreted as an integer"
    try:
        operation = MiningOperation(
            mining_truck_count = 'a',
            mining_station_count = 1).StartOperation()
    except TypeError as e:
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_0_station():
    '''Negative Test case to test of 0 stations input'''

    print('\n\n\n=================================== test_negative_0_station ============================================================')
    error_message = ''
    expected_message = 'One of the key information is missing to start the operation!\nMining Truck Count = 1\nMining Stations Count = 0\nOperation length = 4320'
    try:
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 0).StartOperation()
    except AssertionError as e:
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_stations_negative_value():
    '''Negative Test case to test of -1 stations input'''

    print('\n\n\n=================================== test_negative_stations_negative_value ==============================================')
    error_message = ''
    expected_message = 'One of the key information is missing to start the operation!\nMining Truck Count = 1\nMining Stations Count = 0\nOperation length = 4320'
    try:
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = -1).StartOperation()
    except AssertionError as e:
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_stations_input_type():
    '''Negative Test case to test stations input type'''

    print('\n\n\n=================================== test_negative_stations_input_type ==================================================')
    error_message = ''
    expected_message = "'str' object cannot be interpreted as an integer"
    try:
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 'a').StartOperation()
    except TypeError as e:
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_0_operation_length():
    '''Negative Test case to test of 0 operation length input'''

    print('\n\n\n=================================== test_negative_0_operation_length ===================================================')
    error_message = ''
    expected_message = 'One of the key information is missing to start the operation!\nMining Truck Count = 1\nMining Stations Count = 1\nOperation length = 0'
    try:
        original_operation_length = GlobalConstants.OPERATION_LENGTH
        GlobalConstants.OPERATION_LENGTH = 0
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 1).StartOperation()
    except AssertionError as e:
        GlobalConstants.OPERATION_LENGTH = original_operation_length
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_operation_length_negative_value():
    '''Negative Test case to test of -1 operation length input'''

    print('\n\n\n=================================== test_negative_operation_length_negative_value ======================================')
    error_message = ''
    expected_message = 'One of the key information is missing to start the operation!\nMining Truck Count = 1\nMining Stations Count = 1\nOperation length = -1'
    try:
        original_operation_length = GlobalConstants.OPERATION_LENGTH
        GlobalConstants.OPERATION_LENGTH = -1
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 1).StartOperation()
    except AssertionError as e:
        GlobalConstants.OPERATION_LENGTH = original_operation_length
        error_message = e.args[0]
    assert error_message == expected_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message: {expected_message}')


def test_negative_operation_length_input_type():
    '''Negative Test case to test operation length input type'''

    print('\n\n\n=================================== test_negative_operation_length_input_type ==========================================')
    error_message = ''
    expected_message_part = "not supported between instances of"
    try:
        original_operation_length = GlobalConstants.OPERATION_LENGTH
        GlobalConstants.OPERATION_LENGTH = 'OPERATION_LENGTH'
        MiningOperation(
            mining_truck_count = 1,
            mining_station_count = 1).StartOperation()
    except TypeError as e:
        GlobalConstants.OPERATION_LENGTH = original_operation_length
        error_message = e.args[0]
    assert expected_message_part in error_message, Logger.Log(f'The error message is not the expected one!\nActual message: {error_message}\nExpected message part: {expected_message_part}')


def test_positive_10_trucks_10_stations():
    '''Test case to test behavior with 10 trucks and 10 stations
       Intended to test normal behavior'''

    print('\n\n\n================================== test_positive_10_trucks_10_stations =================================================')
    result = MiningOperation(
        mining_truck_count = 10,
        mining_station_count = 10).StartOperation()
    assert result, Logger.Log('Test failed to finish as intended!')


def test_positive_5000_trucks_10_stations():
    '''Test case to test behavior with 5000 trucks and 10 stations
       Intended to test load balancing and wait time handling behavior and the stopping when wait times
       extends above operation length'''

    print('\n\n\n=================================== test_positive_1000_trucks_1_stations ===============================================')
    result = MiningOperation(
        mining_truck_count = 5000,
        mining_station_count = 10).StartOperation()
    assert result, Logger.Log('Test failed to finish as intended!')
