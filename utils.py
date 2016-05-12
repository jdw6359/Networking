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
  return os.system('ping -c 4 ' + str(address))

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
  # TODO: refactor repo path to environment variable
  repo_path = '/home/tina/Documents/repos/networking'
  gd = '--git-dir=' + os.path.join(repo_path, '.git')
  wt = '--work-tree=' + repo_path

  args = ['git', gd, wt, 'rev-parse', 'HEAD']

  return subprocess.check_output(args).replace('\n','')

def testDriver():
  print monitoringVersion()
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

