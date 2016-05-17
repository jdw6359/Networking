# Libraries for making web requests
import urllib
import urllib2
# Create Datetime objects
import datetime
# Communicate with OS
import os
# Used for putting script to sleep
import time

import utils
from CheckInUtil import *
from DowntimeSegmentUtil import *
from FleetMonitorClient import *

class NetworkStatus():
    def __init__(self, defaultRouterActive, cellRouterActive,
        remoteDNSActive, remoteSiteActive):
        
        self.__defaultRouterActive = defaultRouterActive
        self.__cellRouterActive = cellRouterActive
        self.__remoteDNSActive = remoteDNSActive
        self.__remoteSiteActive = remoteSiteActive

    def __str__(self):
        status = ''
        if self.isAvailable():
            status = 'Available'
        else:
            if(not self.__defaultRouterActive):
                status = 'Default Router Down'
            if(not self.__cellRouterActive):
                if status != '':
                    status += ', '
                status += 'Cell Router Down'
            if(not self.__remoteDNSActive):
                if status != '':
                    status += ', '
                status += 'Remote DNS Down'
            if(not self.__remoteSiteActive):
                if status != '':
                    status += ', '
                status += 'Remote Site Down'
        return status

    @property
    def defaultRouterActive(self):
        return self.__defaultRouterActive

    @property
    def cellRouterActive(self):
        return self.__cellRouterActive

    @property
    def remoteDNSActive(self):
        return self._remoteDNSActive

    @property
    def remoteSiteActive(self):
        return self.__remoteSiteActive

    def isAvailable(self):
        return (self.__defaultRouterActive and self.__cellRouterActive
            and self.__remoteDNSActive and self.__remoteSiteActive)

def checkStatus():
    defaultRouterActive = False
    cellRouterActive = False
    remoteDNSActive = False
    remoteSiteActive = False

    # determine gatewayAddress
    # TODO: fix utils.getDefaultGateway() - not getting correct value when wifi down
    defaultRouterAddress = utils.getDefaultGateway()
    print 'default router address: ' + str(defaultRouterAddress)
    print 'pinging default router...' + str(defaultRouterAddress)
    
    pingResponse = utils.pingAddress(defaultRouterAddress)
    if pingResponse == 0:
        print 'response from ping: ', pingResponse
        defaultRouterActive = True
    else:
        print 'no responses from ping!'

    # ping the cell router
    #TODO: change cellRouterAddress
    cellRouterAddress = utils.getDefaultGateway()
    #cellRouterAddress = '10.123.123.33'
    print 'cell router address: ' + str(cellRouterAddress)
    print 'pinging cell router...' + str(cellRouterAddress)
    pingResponse = utils.pingAddress(cellRouterAddress)
    if pingResponse == 0:
        print 'response from ping: ', pingResponse
        cellRouterActive = True
    else:
        print 'no responses from ping!'


    # ping remove DNS server
    remoteDNSAddress = '8.8.8.8'
    print 'pinging remote dns address: ' + str(remoteDNSAddress)
    pingResponse = utils.pingAddress(remoteDNSAddress)
    if pingResponse == 0:
        print 'response from ping: ', pingResponse
        remoteDNSActive = True
    else:
        print 'no response from ping!'


    # make http request 
    remoteSiteAddress = 'http://python.org/'
    print 'sending http request to remote site: ' + str(remoteSiteAddress)
    try:
        response = urllib2.urlopen(remoteSiteAddress)
        print 'response object: ' + str(response)
        # Determine how the http response will drive
        # remoteSiteActive value
        code = response.getcode()
        print 'response code: ' + str(code)
        # TODO: refactor the interpretation of response / code
        if(code == 200):
            remoteSiteActive = True
    except urllib2.URLError:
        remoteSiteActive = False


    # TODO: remove this
    # defaultRouterActive = True

    print 'status check results...'
    print '[Default Router Active]: ' + str(defaultRouterActive)
    print '[Cell Router Active]: ' + str(cellRouterActive)
    print '[Remote DNS Active]: ' + str(remoteDNSActive)
    print '[Remote Site Active]: ' + str(remoteSiteActive)

    return NetworkStatus(defaultRouterActive, cellRouterActive,
        remoteDNSActive, remoteSiteActive)

'''
Take action depending on the network status
'''
def handleResults(networkStatus):
    # Instantiate new downtime segment util
    downtimeSegmentUtil = DowntimeSegmentUtil()

    if(networkStatus.defaultRouterActive):
        # Check to see if the defaultRouter has JUST become available
        if(downtimeSegmentUtil.downtimeSegmentActive()):
            print 'default router has JUST become available'
            # TODO: issue commands to switch via telnet
            # - reconfigure network to use defaultRouter as gateway
            
            # TODO: MAKE SURE that network has been properly reconfigured
            # before ending downtime, otherwise posting of downtime segment
            # will likely fail
            downtimeSegmentUtil.endDowntime()

    else:
        # If there is not an active downtime segment,
        # we have JUST lost defaultRouter availability
        if(not downtimeSegmentUtil.downtimeSegmentActive()):
            print 'default router has JUST gone down'
            downtimeSegmentUtil.startDowntime()
            # TODO: issue commands to switch via telnet
            # - reconfigure network to use cellRouter as gateway
            # switchAddress = '10.123.123.35'

'''
Attempt to write the results up to the web service
'''
def writeResults(status):
    # Create a new FleetMonitorClient instance
    fleetMonitorClient = FleetMonitorClient()
    fleetMonitorClient.postCheckIn(status)

def main():
    print 'starting status check...'

    # Determine the status by polling the various sources
    for i in range (3):
        print 'about to check status'
        networkStatus = checkStatus()
        print 'about to check status available...'
        if networkStatus.isAvailable():
            break
        else:
            print 'sleeping'
            time.sleep(5)
            print 'done sleeping'

    # take action depending on the results of the network status
    handleResults(networkStatus)
    # write the results to the web service
    writeResults(str(networkStatus))
main()

# need to tell script which vlan to run ping out of

# need to check that cell router is up - make sure it is up
# need to perform same set of checks on cell device as the default gateway

# only perform communication with web service through default connection
# report same metrics
