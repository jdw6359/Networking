import subprocess
import os

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



print 'status check results...'
print '[Gateway Active]: ' + str(gatewayActive)
print '[Remote DNS Active]: ' + str(remoteDNSActive)
print '[Remote Site Active]: ' + str(remoteSiteActive)

