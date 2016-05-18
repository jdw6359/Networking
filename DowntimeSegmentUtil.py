import datetime
import os
from FleetMonitorClient import *
import logging

'''
Utility for interacting with downtime segment file
'''
class DowntimeSegmentUtil():
    def __init__(self):
        # TODO: change this path to more conventional system
        # location as opposed to inside codebase
        self.filePath = str(os.environ['BINARY_PROJECT_PATH']) + '/downtime_segment.txt'

    '''
    Write current time to file to mark the start of downtime
    '''
    def startDowntime(self):
        logging.warning('[Downtime Segment] starting ...')
        with open(self.filePath, 'w') as downtimeSegmentFile:
            downtimeSegmentStartTime = str(datetime.datetime.now())
            downtimeSegmentFile.write(downtimeSegmentStartTime)
        logging.warning('[Downtime Segment] downtime started at %s', downtimeSegmentStartTime)

    '''
    Determine start and end time of downtime segment, traffic through
    cell router, write results to fleet monitor, flush tmp downtime file
    '''
    def endDowntime(self):
        # get the start time of the downtime segment
        with open(self.filePath) as downtimeSegmentFile:
            downtimeSegmentStartTime = downtimeSegmentFile.read()

        # end time of the downtime segment is based on current time
        downtimeSegmentEndTime = str(datetime.datetime.now())

        logging.warning('[Downtime Segment] ending ... %s', str(downtimeSegmentEndTime))

        # TODO: determine how many bytes of data have been consumed
        # by cell router during the course of the downtime segment
        bytesTraffic = 1234

        logging.warning('[Downtime Segment] downtime ranging from %s - %s', downtimeSegmentStartTime, downtimeSegmentEndTime)
        logging.warning('[Downtime Segment] bytes of traffic through cell router: %s', str(bytesTraffic))
        logging.warning('[Downtime Segment] writing segment data to fleet monitor...')

        fleetMonitorClient = FleetMonitorClient()
        fleetMonitorClient.postDowntimeSegment(downtimeSegmentStartTime,
            downtimeSegmentEndTime, bytesTraffic)

        # remove the downtime segment tmp file
        os.remove(self.filePath)

    '''
    Inspects contents of downtime segment util to determine if
    default connection was previously down or if this is the first
    segment without a default connection.
    '''
    def downtimeSegmentActive(self):
        # If the backup segment text file does not exist,
        # then the default connection has just gone down
        return os.path.isfile(self.filePath)

if(__name__ == '__main__'):
    # Test functionality here
    downtimeSegmentUtil = DowntimeSegmentUtil()
    