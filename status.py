import subprocess
import os
import urllib2

print 'starting status check...'

gatewayActive = False
remoteDNSActive = False
remoteSiteActive = False

# determine gatewayAddress
gatewayAddress = subprocess.check_output(['./gateway.sh'])
print 'gateway address: ' + str(gatewayAddress)
print 'pinging gateway...' + str(gatewayAddress)
response = os.system('ping -c 4 ' + str(gatewayAddress))
# ping command returns non-zero response when successful
if response == 0:
    print 'response from ping: ', response
    gatewayActive = True
else:
    print 'no responses from ping!'

# ping remove DNS server
remoteDNSAddress = '8.8.8.8'
print 'pinging remote dns address: ' + str(remoteDNSAddress)
response = os.system('ping -c 4 ' + str(remoteDNSAddress))
if response == 0:
    print 'response from ping: ', response
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

if(code == 200):
    remoteSiteActive = True


print 'status check results...'
print '[Gateway Active]: ' + str(gatewayActive)
print '[Remote DNS Active]: ' + str(remoteDNSActive)
print '[Remote Site Active]: ' + str(remoteSiteActive)

