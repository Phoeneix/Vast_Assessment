'''The file for the mining operation optimization'''

import random

from config.global_constants import GlobalConstants
from logger.enums import LogLevel
from logger.logger import Logger
from mining_operation.enums import TruckStatus
from mining_operation.report_generator import ReportGenerator


class MiningOperation():
    '''Class for mining operation'''

    # Constants
    UNLOAD_TIME = 5         # The Mining Trucks unload time
    TRAVEL_TIME = 30        # The Mining Trucks travel time to the stations

    def __init__(self,
                 mining_truck_count:int,
                 mining_station_count:int) -> None:
        '''Initialize the mining operation'''

        # Get the mining time for each truck on the site
        self.mining_trucks = {}
        self._mining_trucks_history = {}
        for i in range(mining_truck_count):
            mining_length = GetMiningLength()
            self.mining_trucks[i] = (TruckStatus.MINING, mining_length)
            self.mining_trucks_history = i, self.mining_trucks[i]

        # Setting up the mining stations
        self.mining_stations = {}
        for i in range(mining_station_count):
            self.mining_stations[i] = {}

        # Setting the elapsed time to 0
        self.elapsed_time = 0

        # Setting the operation lenght constant
        self.operation_ended = False


    @property
    def elapsed_time(self) -> int:
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value:int):
        self._elapsed_time = value


    @property
    def mining_trucks(self) -> dict:
        return self._mining_trucks

    @mining_trucks.setter
    def mining_trucks(self, value:dict):
        self._mining_trucks = value


    @property
    def mining_trucks_history(self) -> dict:
        return self._mining_trucks_history

    @mining_trucks_history.setter
    def mining_trucks_history(self, value):
        if type(value) is dict:
            self._mining_trucks_history = value
        elif type(value) is tuple:
            truck_id, data = value
            if truck_id not in self._mining_trucks_history:
                self._mining_trucks_history[truck_id] = {}
                latest_event_id = 0
            else:
                latest_event_id = int(max(self._mining_trucks_history[truck_id]))
            self._mining_trucks_history[truck_id][latest_event_id + 1] = data


    @property
    def mining_stations(self) -> dict:
        return self._mining_stations

    @mining_stations.setter
    def mining_stations(self, value:dict):
        self._mining_stations = value


    @property
    def operation_ended(self) -> bool:
        return self._operation_ended

    @operation_ended.setter
    def operation_ended(self, value:bool):
        self._operation_ended = value


    def StartOperation(self) -> bool:
        '''Method to execute the mining operation'''

        mining_trucks_count = len(self.mining_trucks)
        mining_stations_count = len(self.mining_stations)

        if GlobalConstants.LOG_LEVEL in [LogLevel.INFO, LogLevel.DEBUG]:
            Logger.Log(f'\n==================================== Operation Started ====================================\n')
            Logger.Log(f'Logging level: {GlobalConstants.LOG_LEVEL.name}')
            Logger.Log(f'Operation length: {GlobalConstants.OPERATION_LENGTH}')
            Logger.Log(f'Mining Trucks count: {mining_trucks_count}')
            Logger.Log(f'Mining Stations count: {mining_stations_count}\n')

        assert not (mining_trucks_count <= 0 or \
            mining_stations_count <= 0 or \
            GlobalConstants.OPERATION_LENGTH <= 0), \
            Logger.Log(f'One of the key information is missing to start the operation!\nMining Truck Count = {mining_trucks_count}\nMining Stations Count = {mining_stations_count}\nOperation length = {GlobalConstants.OPERATION_LENGTH}')
        while self.elapsed_time <= GlobalConstants.OPERATION_LENGTH and not self.operation_ended:

            # Get the truck that will finish it's job next and when
            truck_id = self.FindNextTruckToFinish()
            time_forward = self.mining_trucks[truck_id][1]

            # Forward all the truck's time to that point
            self.ForwardTimeWith(time_forward)
            if self.operation_ended:
                break

            # Update the truck's status that will finish it's job to the next job
            if self.mining_trucks[truck_id][1] == 0:
                self.UpdateTruckStatus(truck_id)

        # Generate the reports for the operation
        ReportGenerator.GenerateForMiningTrucks(self.mining_trucks_history)
        ReportGenerator.GenerateForMiningStations(self.mining_stations)
        if GlobalConstants.LOG_LEVEL in [LogLevel.INFO, LogLevel.DEBUG]:
            Logger.Log(f'\n\n\n==================================== Operation Ended ====================================')
        return True


    def FindNextTruckToFinish(self) -> str:
        '''Method to find out which mining trucks will have an event next'''

        truck_data_to_finish_next = ()
        # print(f'mining_trucks: {self.mining_trucks}')
        for truck_id in self.mining_trucks:
            # Extract the data of the truck
            truck_data = self.mining_trucks[truck_id]
            time_left = truck_data[1]
            truck_status = truck_data[0]
            if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
                Logger.Log(f'truck_id: {truck_id}, status: {truck_status}, time_left: {time_left}')
                Logger.Log(f'truck_data_to_finish_next: {truck_data_to_finish_next}')

            if truck_data_to_finish_next == ():
                # If it's the first truck save it as the base for comparison
                truck_data_to_finish_next = (truck_id, time_left)
            elif time_left < truck_data_to_finish_next[1]:
                # Compare the time left with the saved one's, and if it's lower then switch it.
                truck_data_to_finish_next = (truck_id, time_left)

        if truck_data_to_finish_next != ():
            return truck_data_to_finish_next[0]
        else:
            return None


    def ForwardTimeWith(self, time_forward:int):
        '''Method to forward the time for all the mining trucks'''

        for truck_id in self.mining_trucks:
            current_time = self.mining_trucks[truck_id][1]
            new_time = current_time - time_forward
            truck_status = self.mining_trucks[truck_id][0]
            self.mining_trucks[truck_id] = (truck_status, new_time)

        # Increase the elapsed time to reflect the timeline correctly
        self.elapsed_time += time_forward
        if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
            Logger.Log(f'\nTime forwarded: {time_forward}\n')
        if GlobalConstants.OPERATION_LENGTH <= self.elapsed_time:
            self.operation_ended = True



    def UpdateTruckStatus(self, truck_id:str):
        '''Method to update the mining truck with the next job's data'''

        status = self.mining_trucks[truck_id][0]

        # If it was mining, switch to traveling and add the travel time
        if status is TruckStatus.MINING:
            new_status = TruckStatus.TRAVELING_TO_STATION
            new_value = self.TRAVEL_TIME

        # If it was traveling, switch to queue up for mining station and add wait time
        elif status is TruckStatus.TRAVELING_TO_STATION:
            new_status = TruckStatus.WAITING_AT_STATION
            new_value = self.QueueForStation(truck_id)

        # If it was queued, switch to unloading and add the unloading time
        elif status is TruckStatus.WAITING_AT_STATION:
            new_status = TruckStatus.UNLOADING
            new_value = self.UNLOAD_TIME

        # If it was unloading, switch to traveling and add the travel time
        elif status is TruckStatus.UNLOADING:
            new_status = TruckStatus.TRAVELING_TO_SITE
            new_value = self.TRAVEL_TIME

        # If it was traveling, switch to mining and generate a mining time
        elif status is TruckStatus.TRAVELING_TO_SITE:
            new_status = TruckStatus.MINING
            new_value = GetMiningLength()
        else:
            raise NotImplementedError(f'Status "{status}" handling not implemented!')

        if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
            Logger.Log(f'\nTruck #{truck_id} changing to: {new_status} for {new_value}\n')
        self.mining_trucks[truck_id] = (new_status, new_value)
        self.mining_trucks_history = truck_id, (new_status, new_value)


    def QueueForStation(self, truck_id:str) -> int:
        '''Method to get the wait time for the truck at the station'''

        current_time = self.elapsed_time
        next_free_station = ()
        # Go through all the stations to find the one it can queue the truck for
        for station_id in self.mining_stations:
            if len(self.mining_stations[station_id]) == 0:
                latest_available_time = 0
            else:
                latest_available_time = max(self.mining_stations[station_id])

            if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
                Logger.Log(f'\nStation #{station_id} last unloading spot: {latest_available_time}')
                Logger.Log(f'Current time: {current_time}')
            # If the last unloading finish is lower then the current time, then the station is free
            if latest_available_time < current_time:
                next_free_station = (station_id, 0)
                if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
                    Logger.Log(f'Station #{station_id} is free')
                break
            # If it wasn't free, but it's the first station, save the name and available time
            elif next_free_station == ():
                next_free_station = (station_id, latest_available_time)
            # If the available time is lower then the lowest previous station's,
            # then update which station will be free soonest
            elif latest_available_time < next_free_station[1]:
                next_free_station = (station_id, latest_available_time)
            if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
                Logger.Log(f'Next free station {next_free_station}')

        # Calculate the wait time by distracting the current time from the latest available time
        if next_free_station[1] == 0:
            wait_time = next_free_station[1]
        else:
            wait_time = next_free_station[1] - current_time + 1

        # Add truck unloading time to the station
        self.UpdateStationStatus(truck_id, next_free_station[0], wait_time)

        if GlobalConstants.OPERATION_LENGTH < wait_time + current_time:
            self.operation_ended = True
        return wait_time


    def UpdateStationStatus(self, truck_id:str, station_id:str, wait_time:int):
        '''Method to update the mining station with the incoming truck's data'''

        # Get the time stamp for the start and end time of the unloading of the truck at the station
        star_time = self.elapsed_time + wait_time
        end_time = star_time + self.UNLOAD_TIME

        # Add the time stamps to the station's queue, so other trucks will know those time slots are taken by which truck
        for time_stamp in range(star_time, end_time):
            if GlobalConstants.OPERATION_LENGTH < time_stamp:
                break
            self.mining_stations[station_id][time_stamp] = truck_id
            if GlobalConstants.LOG_LEVEL in [LogLevel.DEBUG]:
                Logger.Log(f'Station #{station_id} reserving time slot {time_stamp} to truck #{truck_id}')


def GetMiningLength(min_length:int=60, max_length:int=300) -> int:
    '''Private method to get a randimized number for mining'''

    return random.randint(min_length, max_length)
