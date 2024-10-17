'''The file for the mining operation optimization'''

import random

from mining_operation.enums import TruckStatus


class MiningOperation():
    '''Class for mining operation'''

    # Constants
    UNLOAD_TIME = 5         # The Mining Trucks unload time
    TRAVEL_TIME = 30        # The Mining Trucks travel time to the stations
    OPERATION_LENGTH = 0    # The Mining Operation's length

    def __init__(self,
                 mining_truck_count:int,
                 mining_station_count:int,
                 operation_length:int) -> None:
        '''Start the mining operation'''

        # Get the mining time for each truck on the site
        self.mining_trucks = {}
        for i in range(mining_truck_count):
            mining_length = GetMiningLength()
            self.mining_trucks[i] = (TruckStatus.MINING, mining_length)

        # Setting up the mining stations
        self.mining_stations = {}
        for i in range(mining_station_count):
            self.mining_stations[i] = {}

        # Setting the elapsed time to 0
        self.elapsed_time = 0

        # Setting the operation lenght constant
        self.OPERATION_LENGTH = operation_length
        self.kill_switch = False


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
        print(f'Setter value: {value}')
        self._mining_trucks = value


    @property
    def mining_stations(self) -> dict:
        return self._mining_stations

    @mining_stations.setter
    def mining_stations(self, value:dict):
        self._mining_stations = value


    @property
    def kill_switch(self) -> bool:
        return self._kill_switch

    @kill_switch.setter
    def kill_switch(self, value:bool):
        self._kill_switch = value


    def FlowOrganizer(self) -> bool:
        '''Method to follow the current status of the mining operation'''

        mining_trucks_count = len(self.mining_trucks)
        mining_stations_count = len(self.mining_stations)
        print(f'OPERATION_LENGTH: {self.OPERATION_LENGTH}')
        print(f'Mining Trucks count: {mining_trucks_count}')
        print(f'Mining Stations count: {mining_stations_count}')
        assert not (mining_trucks_count == 0 or \
            mining_stations_count == 0 or \
            self.OPERATION_LENGTH == 0), \
            f'One of the key information is missing to start the operation!\nMining Truck Count = {mining_trucks_count}\nMining Stations Count = {mining_stations_count}\nOperation length = {self.OPERATION_LENGTH}'
        while self.elapsed_time <= self.OPERATION_LENGTH and not self.kill_switch:

            # Get the truck that will finish it's job next and when
            truck_name = self.FindNextTruckToFinish()
            time_forward = self.mining_trucks[truck_name][1]

            # Forward all the truck's time to that point
            self.ForwardTimeWith(time_forward)

            # Update the truck's status that will finish it's job to the next job
            if self.mining_trucks[truck_name][1] == 0:
                self.UpdateTruckStatus(truck_name)

            # print(f'Trucks status: {self.mining_trucks}\n')
            # print(f'Station status: {self.mining_stations}\n')

        return True


    def FindNextTruckToFinish(self) -> str:
        '''Method to find out which mining trucks will have an event next'''

        truck_data_to_finish_next = ()
        # print(f'mining_trucks: {self.mining_trucks}')
        for truck_name in self.mining_trucks:
            # Extract the data of the truck
            truck_data = self.mining_trucks[truck_name]
            time_left = truck_data[1]
            truck_status = truck_data[0]
            # print(f'truck_name: {truck_name}')
            # print(f'truck_status: {truck_status}')
            # print(f'time_left: {time_left}')
            # print(f'truck_data_to_finish_next: {truck_data_to_finish_next}')

            if truck_data_to_finish_next == ():
                # If it's the first truck save it as the base for comparison
                truck_data_to_finish_next = (truck_name, time_left)
            elif time_left < truck_data_to_finish_next[1]:
                # Compare the time left with the saved one's, and if it's lower then switch it.
                truck_data_to_finish_next = (truck_name, time_left)

        if truck_data_to_finish_next != ():
            return truck_data_to_finish_next[0]
        else:
            return None


    def ForwardTimeWith(self, time_forward:int):
        '''Method to forward the time for all the mining trucks'''

        for truck_name in self.mining_trucks:
            current_time = self.mining_trucks[truck_name][1]
            new_time = current_time - time_forward
            truck_status = self.mining_trucks[truck_name][0]
            self.mining_trucks[truck_name] = (truck_status, new_time)

        # Increase the elapsed time to reflect the timeline correctly
        self.elapsed_time += time_forward


    def UpdateTruckStatus(self, truck_name:str):
        '''Method to update the mining truck with the next job's data'''

        status = self.mining_trucks[truck_name][0]

        # If it was mining, switch to traveling and add the travel time
        if status is TruckStatus.MINING:
            new_status = TruckStatus.TRAVELING_TO_STATION
            new_value = self.TRAVEL_TIME

        # If it was traveling, switch to queue up for mining station and add wait time
        elif status is TruckStatus.TRAVELING_TO_STATION:
            new_status = TruckStatus.WAITING_AT_STATION
            new_value = self.QueueForStation(truck_name)

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

        self.mining_trucks[truck_name] = (new_status, new_value)


    def QueueForStation(self, truck_name:str) -> int:
        '''Method to get the wait time for the truck at the station'''

        current_time = self.elapsed_time
        next_free_station = ()
        # Go through all the stations to find the one it can queue the truck for
        for station_name in self.mining_stations:
            if len(self.mining_stations[station_name]) == 0:
                latest_available_time = 0
            else:
                latest_available_time = max(self.mining_stations[station_name])

            # If the last unloading finish is lower then the current time, then the station is free
            if latest_available_time < current_time:
                next_free_station = (station_name, 0)
                break
            # If it wasn't free, but it's the first station, save the name and available time
            elif next_free_station == ():
                next_free_station = (station_name, latest_available_time)
            # If the available time is lower then the lowest previous station's,
            # then update which station will be free soonest
            elif latest_available_time < next_free_station[1]:
                next_free_station = (station_name, latest_available_time)

        # Calculate the wait time by distracting the current time from the latest available time
        if next_free_station[1] == 0:
            wait_time = next_free_station[1]
        else:
            wait_time = next_free_station[1] - current_time + 1

        # Add truck unloading time to the station
        self.UpdateStationStatus(truck_name, next_free_station[0], wait_time)

        print(f'wait_time: {wait_time}')
        if self.OPERATION_LENGTH < wait_time + current_time:
            self.kill_switch = True
        return wait_time


    def UpdateStationStatus(self, truck_name:str, station_name:str, wait_time:int):
        '''Method to update the mining station with the incoming truck's data'''

        # Get the time stamp for the start and end time of the unloading of the truck at the station
        star_time = self.elapsed_time + wait_time
        end_time = star_time + self.UNLOAD_TIME

        # Add the time stamps to the station's queue, so other trucks will know those time slots are taken by which truck
        for time_stamp in range(star_time, end_time):
            self.mining_stations[station_name][time_stamp] = truck_name


def GetMiningLength(min_length:int=60, max_length:int=300) -> int:
    return random.randint(min_length, max_length)
