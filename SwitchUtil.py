'''
Communication utility with switch
'''

import os
import sys
import telnetlib

class SwitchUtil():
	def __init__(self):
		self.__address = '10.123.123.35'

	@property
	def address(self):
		return self.__address

	def changeVlan(self, vlan):
		# Instantiate telnet client
		tn = telnetlib.Telnet(self.__address)

		print tn.read_until('Username: ')
		tn.write('admin\n')

		print tn.read_until('Password: ')
		tn.write('1pmlamsh\n')

		print tn.read_until('bid-sw-001>')
		tn.write('ena\n')

		print tn.read_until('Password: ')
		tn.write('1pmlamsh\n')

		print tn.read_until('bid-sw-001#')
		tn.write('config t\n')

		print tn.read_until('bid-sw-001(config)#')
		tn.write('int GigabitEthernet0/8\n')

		print tn.read_until('bid-sw-001(config-if)#')
		tn.write('switchport access vlan ' + str(vlan) + '\n')

		print tn.read_until('bid-sw-001(config-if)#')
		tn.write('exit\n')

		print tn.read_until('bid-sw-001(config)#')
		tn.write('exit\n')

		print tn.read_until('bid-sw-001#')
		tn.write('exit\n')		

		print 'done!'

	def useDefaultRouter(self):
		print 'use default router invoked...'
		print 'change vlan invoked with 900'
		self.changeVlan(900)

	def useCellRouter(self):
		print 'use cell router invoked...'
		print 'change vlan invoked with 902'
		self.changeVlan(902)


if (__name__ == '__main__'):
	util = SwitchUtil()
	util.useDefaultRouter()
