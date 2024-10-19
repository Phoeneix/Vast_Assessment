'''The file for the mining operation's report generation'''

from config.global_constants import GlobalConstants
from mining_operation.enums import TruckStatus
from utils.file_handler import FileHandler


class ReportGenerator():
    '''Class for generating reports'''

    def GenerateForMiningTrucks(mining_trucks:dict):
        '''Method to generate a report for the mining trucks'''

        report = {}

        # Going through all the trucks and generate reports for each one
        for truck_id in mining_trucks:
            report[truck_id] = ReportGenerator.GenerateForSingleTruck(
                truck_id = truck_id,
                truck_data = mining_trucks[truck_id])
        report['summary'] = ReportGenerator.CreateSummary(report)
        ReportGenerator.SaveReportToFile(report)
        ReportGenerator.PrintReport(report)


    def GenerateForMiningStations(mining_stations:dict):
        '''Method to generate a report for the mining trucks'''

        report = {}

        # Going through all the stations and generate reports for each one
        for station_id in mining_stations:
            report[station_id] = ReportGenerator.GenerateForSingleStation(
                station_id = station_id,
                station_data = mining_stations[station_id])
        report['summary'] = ReportGenerator.CreateSummary(report)
        ReportGenerator.SaveReportToFile(report)
        ReportGenerator.PrintReport(report)


    def GenerateForSingleTruck(truck_id:int, truck_data:dict) -> dict:
        '''Method to generate a report for a single truck'''

        result = {'report': '',
            'mining_time': 0,
            'travel_time': 0,
            'wait_time': 0,
            'unload_time': 0,
            'total_time': 0}

        # Go through all the truck's events and categorize them
        for event_id in truck_data:
            truck_status, time_spent = truck_data[event_id]
            result['total_time'] += time_spent

            # To remove the excess time after the operation ended, so it will not distort the values
            if GlobalConstants.OPERATION_LENGTH < result['total_time']:
                time_spent -= (result['total_time'] - GlobalConstants.OPERATION_LENGTH)
                result['total_time'] = GlobalConstants.OPERATION_LENGTH
            if truck_status is TruckStatus.MINING:
                result['mining_time'] += time_spent
            elif truck_status is TruckStatus.TRAVELING_TO_STATION:
                result['travel_time'] += time_spent
            elif truck_status is TruckStatus.WAITING_AT_STATION:
                result['wait_time'] += time_spent
            elif truck_status is TruckStatus.UNLOADING:
                result['unload_time'] += time_spent
            elif truck_status is TruckStatus.TRAVELING_TO_SITE:
                result['travel_time'] += time_spent

        # Create the report formatting
        report = f'\n===== Mining Truck History for truck #{truck_id} =====\n'
        report += f'Total time spent: {result["total_time"]}\n'
        report += f'Time spent MINING: {result["mining_time"]} ({(result["mining_time"] / result["total_time"])*100:.2f}%)\n'
        report += f'Time spent TRAVELING: {result["travel_time"]} ({(result["travel_time"] / result["total_time"])*100:.2f}%)\n'
        report += f'Time spent WAITING: {result["wait_time"]} ({(result["wait_time"] / result["total_time"])*100:.2f}%)\n'
        report += f'Time spent UNLOADING: {result["unload_time"]} ({(result["unload_time"] / result["total_time"])*100:.2f}%)\n'

        result['report'] = report
        return result


    def GenerateForSingleStation(station_id:int, station_data:dict) -> dict:
        '''Method to generate a report for a single station'''

        result = {'report': '',
            'unload_time': 0,
            'wait_time': 0,
            'total_time': GlobalConstants.OPERATION_LENGTH}

        # Go the information how busy the station was
        result['unload_time'] = len(station_data)
        result['wait_time'] = GlobalConstants.OPERATION_LENGTH - len(station_data)
        if len(station_data) == 0:
            result['first_unload_time'] = 'None arrived'
        else:
            result['first_unload_time'] = min(station_data)

        # Create the report formatting
        report = f'\n===== Mining Station History for station #{station_id} =====\n'
        report += f'First truck arrived at the station: {result["first_unload_time"]}\n'
        report += f'Time spent WAITING: {result["wait_time"]} ({(result["wait_time"] / result["total_time"])*100:.2f}%)\n'
        report += f'Time spent UNLOADING: {result["unload_time"]} ({(result["unload_time"] / result["total_time"])*100:.2f}%)\n'

        result['report'] = report
        return result


    def CreateSummary(report:dict) -> dict:
        '''Method to generate a report summary'''

        result = {}

        # Summing the different activities
        for id in report:
            for status_id in report[id]:
                if status_id == 'report':
                    continue
                if status_id not in result:
                    result[status_id] = 0
                if isinstance(report[id][status_id], int):
                    result[status_id] += report[id][status_id]

        # Making it the average
        for status_id in result:
            result[status_id] = (result[status_id] / len(report))

        # Create the report formatting
        summary_report = f'\n=========================== Summary ===========================\n'
        if 'mining_time' in result:
            summary_report += f'Average time spent MINING: {result["mining_time"]} ({(result["mining_time"] / result["total_time"])*100:.2f}%)\n'
        if 'travel_time' in result:
            summary_report += f'Average time spent TRAVELING: {result["travel_time"]} ({(result["travel_time"] / result["total_time"])*100:.2f}%)\n'
        if 'wait_time' in result:
            summary_report += f'Average time spent WAITING: {result["wait_time"]} ({(result["wait_time"] / result["total_time"])*100:.2f}%)\n'
        if 'unload_time' in result:
            summary_report += f'Average time spent UNLOADING: {result["unload_time"]} ({(result["unload_time"] / result["total_time"])*100:.2f}%)'
        summary_report += '\n\n\n'

        result['report'] = summary_report
        return result


    def SaveReportToFile(report:dict):
        '''Method to save the report into a file'''

        for id in report:
            FileHandler.SaveIntoFile(
                content = report[id]['report'],
                file_name = f'report_{GlobalConstants.CURRENT_TIME}.log')


    def PrintReport(report:dict):
        '''Method to print the report into the console'''

        for id in report:
            print(report[id]['report'])
