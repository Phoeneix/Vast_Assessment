'''The file for pytest hooks in this directory'''


def pytest_sessionstart(session):
    '''Hook method which is executing before all tests'''
    print('\n\nExecuting before all hook...\n')


def pytest_sessionfinish(session):
    '''Hook method which is executing after all tests'''
    print('\n\nExecuting after all hook...\n')    