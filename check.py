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

class NetworkStatus():
    def __init__(self, defaultRouterActive, cellRouterActive,
        remoteDNSActive, remoteSiteActive):
        
        self.defaultRouterActive = defaultRouterActive
        self.cellRouterActive = cellRouterActive
        self.remoteDNSActive = remoteDNSActive
        self.remoteSiteActive = remoteSiteActive

    def __str__(self):
        status = ''
        if self.isAvailable():
            status = 'Available'
        else:
            if(not self.defaultRouterActive):
                status = 'Default Router Down'
            if(not self.cellRouterActive):
                if status != '':
                    status += ', '
                status += 'Cell Router Down'
            if(not self.remoteDNSActive):
                if status != '':
                    status += ', '
                status += 'Remote DNS Down'
            if(not self.remoteSiteActive):
                if status != '':
                    status += ', '
                status += 'Remote Site Down'
        return status

    def isAvailable(self):
        return (self.defaultRouterActive and self.cellRouterActive
            and self.remoteDNSActive and self.remoteSiteActive)

def checkStatus():
    defaultRouterActive = False
    cellRouterActive = False
    remoteDNSActive = False
    remoteSiteActive = False

    # determine gatewayAddress
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
    cellRouterAddress = '10.123.123.33'
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
    response = urllib2.urlopen(remoteSiteAddress)
    print 'response object: ' + str(response)

    # Determine how the http response will drive
    # remoteSiteActive value
    code = response.getcode()
    print 'response code: ' + str(code)

    # TODO: refactor the interpretation of response / code
    if(code == 200):
        remoteSiteActive = True


    print 'status check results...'
    print '[Default Router Active]: ' + str(defaultRouterActive)
    print '[Cell Router Active]: ' + str(cellRouterActive)
    print '[Remote DNS Active]: ' + str(remoteDNSActive)
    print '[Remote Site Active]: ' + str(remoteSiteActive)

    return NetworkStatus(defaultRouterActive, cellRouterActive,
        remoteDNSActive, remoteSiteActive)

def writeResults(status):
    BASE_URL = str(os.environ['BINARY_CHECK_IN_URL'])

    checkInUrl = BASE_URL + '/check_ins'

    # TODO: Use MAC address to get device id
    deviceId = str(os.environ['BINARY_DEVICE_ID'])
    time = str(datetime.datetime.now())
    monitoring_version = str(utils.monitoringVersion())
    os_version = utils.kernelVersion()

    # TODO: Get cell status

    values = dict(device_id=str(deviceId), monitoring_version=monitoring_version,
        os_version=os_version, primary_status=status, cell_status=status, check_in_time=time)
    data = urllib.urlencode(values)
    request = urllib2.Request(checkInUrl, data)
    response = urllib2.urlopen(request)
    content = response.read()

def main():
    print 'starting status check...'

    # Determine the status by polling the various sources
    for i in range (5):
        print 'about to check status'
        status = checkStatus()
        print 'about to check status available...'
        if status.isAvailable():
            break
        else:
            print 'sleeping'
            time.sleep(5)
            print 'done sleeping'
    writeResults(str(status))
main()

# need to tell script which vlan to run ping out of

# need to check that cell router is up - make sure it is up
# need to perform same set of checks on cell device as the default gateway

# only perform communication with web service through default connection
# report same metrics
