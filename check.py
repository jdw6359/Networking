# Libraries for making web requests
import urllib
import urllib2
# Create Datetime objects
import datetime
# Communicate with OS
import os
# Used for putting script to sleep
import time
import logging

import utils
from SwitchUtil import *
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
    defaultRouterAddress = os.environ['BINARY_DEFAULT_GATEWAY_ADDRESS']
    logging.info('default router address: %s', str(defaultRouterAddress))
    logging.info('pinging default router...%s', str(defaultRouterAddress))
    
    pingResponse = utils.pingAddress(defaultRouterAddress)
    if pingResponse == 0:
        logging.info('response from ping: %s', pingResponse)
        defaultRouterActive = True
    else:
        logging.warning('no responses from ping to %s', defaultRouterAddress)

    # ping the cell router
    #cellRouterAddress = '10.123.123.33'
    cellRouterAddress = os.environ['BINARY_DEFAULT_GATEWAY_ADDRESS']
    logging.info('cell router address: %s', str(cellRouterAddress))
    logging.info('pinging cell router...%s', str(cellRouterAddress))
    pingResponse = utils.pingAddress(cellRouterAddress)
    if pingResponse == 0:
        logging.info('response from ping: %s', pingResponse)
        cellRouterActive = True
    else:
        logging.warning('no responses from ping to %s', cellRouterAddress)


    # ping remove DNS server
    remoteDNSAddress = '8.8.8.8'
    logging.info('pinging remote dns address: %s', remoteDNSAddress)
    pingResponse = utils.pingAddress(remoteDNSAddress)
    if pingResponse == 0:
        logging.info('response from ping: %s', pingResponse)
        remoteDNSActive = True
    else:
        logging.warning('no response from ping %s', remoteDNSAddress)


    # make http request 
    remoteSiteAddress = 'http://python.org/'
    logging.info('sending http request to remote site: %s', remoteSiteAddress)
    try:
        response = urllib2.urlopen(remoteSiteAddress)
        logging.info('response object: %s', str(response))
        # Determine how the http response will drive
        # remoteSiteActive value
        code = response.getcode()
        logging.info('response code: %s', str(code))
        # TODO: refactor the interpretation of response / code
        if(code == 200):
            remoteSiteActive = True
    except urllib2.URLError:
        remoteSiteActive = False

    # TODO: remove this
    # defaultRouterActive = True

    logging.info('status check results...')
    logging.info('[Default Router Active]: %s', str(defaultRouterActive))
    logging.info('[Cell Router Active]: %s', str(cellRouterActive))
    logging.info('[Remote DNS Active]: %s', str(remoteDNSActive))
    logging.info('[Remote Site Active]: %s', str(remoteSiteActive))

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
            logging.warning('default router has JUST become available')
            # TODO: issue commands to switch via telnet
            # - reconfigure network to use defaultRouter as gateway
            
            # instantiate switch util
            switchUtil = SwitchUtil()

            # TODO: wrap in an environment check
            switchUtil.useDefaultRouter()

            # TODO: MAKE SURE that network has been properly reconfigured
            # before ending downtime, otherwise posting of downtime segment
            # will likely fail
            downtimeSegmentUtil.endDowntime()

    else:
        # If there is not an active downtime segment,
        # we have JUST lost defaultRouter availability
        if(not downtimeSegmentUtil.downtimeSegmentActive()):
            logging.warning('default router has JUST gone down')
            downtimeSegmentUtil.startDowntime()
            # TODO: issue commands to switch via telnet
            # - reconfigure network to use cellRouter as gateway

            # instantiate switch util
            switchUtil = SwitchUtil()

            # TODO: invoke commands on switch util (wrap in env check)
            switchUtil.useCellRouter()

'''
Attempt to write the results up to the web service
'''
def writeResults(status):
    # Create a new FleetMonitorClient instance
    fleetMonitorClient = FleetMonitorClient()
    fleetMonitorClient.postCheckIn(status)

def main():
    logging.basicConfig(filename=str(os.environ['BINARY_LOG_FILE']), level=logging.WARNING)
    logging.info('starting status check...')

    # Determine the status by polling the various sources
    for i in range (1):
        logging.info('about to check status')
        networkStatus = checkStatus()
        logging.info('about to check status available...')
        if networkStatus.isAvailable():
            break
        else:
            logging.info('sleeping')
            time.sleep(3)
            logging.info('done sleeping')

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

#TODO store mac address from 'arp 192.168.1.1' in config (mac of default gateway)
#TODO store mac address from 'arp 10.123.123.33' from pi (mac of cell router)
