import subprocess
import os
from uuid import getnode as get

BREAK_LINE = '\n********************\n'

'''
Determines the default gateway using ip route
'''
def getDefaultGateway():
  command = 'ip route'
  args = command.split()
  ipRouteResponse = subprocess.check_output(args).split('\n')
  gatewayLine = ipRouteResponse[0].split()
  defaultGateway = gatewayLine[2]
  return defaultGateway

'''
Pings the provided address.
Non-successful pings return non-zero values
'''
def pingAddress(address):
  return os.system('ping -c 1 ' + str(address))

'''
Grabs the ARP table from machine
'''
def getArpTable():
  command = 'arp'
  args = command.split()
  arpTableResponse = subprocess.check_output(args).split('\n')[1:]
  arpTableList = [x.split() for x in arpTableResponse if (x != '')]
  return arpTableList

'''
Performs an nslookup and get the ip address from the hostname
'''
def getIPFromHostname(hostname):
  command = 'nslookup ' + hostname
  args = command.split()
  ipLookupResponse = subprocess.check_output(args)

  # TODO: return something here
  print ipLookupResponse

'''
Query system for kernel version
'''
def kernelVersion():
  command = 'uname -a'
  args = command.split()
  kernelDetails = subprocess.check_output(args).split()

  #Kernel version is third value of uname response
  return kernelDetails[2]

'''
Execute git command to retrieve commit id of HEAD
'''
def monitoringVersion():
  repo_path = str(os.environ['BINARY_PROJECT_PATH'])

  # When running git commands with crontab, must specify paths
  # to git directory and working tree root
  gd = '--git-dir=' + os.path.join(repo_path, '.git')
  wt = '--work-tree=' + repo_path

  args = ['git', gd, wt, 'rev-parse', 'HEAD']
  return subprocess.check_output(args).replace('\n','')

'''
Get the mac address of the eth0 port
'''
def getMacAddress():
  args = ['ifconfig']

  # TODO: Change this flag to be 'eth0' when on pi
  flag = 'enp0s25'

  ifConfigResponse = subprocess.check_output(args).split('\n')
  for i in range(0,len(ifConfigResponse)):
    # If the current line contains the flag, then look at next line for mac address
    if flag in ifConfigResponse[i]:
      macIndex = i + 1
      break
  # The mac address is the second token in the line following the flag
  return ifConfigResponse[macIndex].split()[1]

def testDriver():

  print getMacAddress()

  '''
  print 'testing utils.getDefaultGateway()...'
  gateway = getDefaultGateway()
  print 'gateway: ' + str(gateway)

  print BREAK_LINE

  print 'testing utils.pingAddress()...'
  pingAddress('8.8.8.8')

  print BREAK_LINE

  print 'testing utils.getARPTable()...'
  arpTable = getArpTable()
  print 'arp table: ' + str(arpTable)

  # arp table is a list records, each their own list of values
  hostname = arpTable[0][0]

  print BREAK_LINE

  print 'testing utils.ipFromHostname()...'
  ipAddress = getIPFromHostname(hostname)
  '''
# If we are executing this file directly execute the following
if(__name__ == "__main__"):
  testDriver()

