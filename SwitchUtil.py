'''
Communication utility with switch
'''

import os
import sys
import logging
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

		logging.info('telnet client created')

		tn.read_until('Username: ')
		tn.write('admin\n')

		logging.info('username prompted and written')

		tn.read_until('Password: ')
		tn.write('1pmlamsh\n')

		logging.info('password prompted and written')

		tn.write('ena\n')
		tn.read_until('Password: ')
		tn.write('1pmlamsh\n')

		logging.info('ena written and password prompted / written')

		tn.write('config t')

		logging.info('config t entered')
		tn.write('int GigabitEthernet0/8\n')
		tn.write('switchport access vlan ' + str(vlan) + ' \n')

		logging.info('vlan switched to 900')
		tn.write('exit')
		tn.write('exit')
		tn.write('exit')
		tn.close()

		logging.info('exited and closed...')

	def useDefaultRouter(self):
		logging.info('use default router invoked...')
		logging.info('change vlan invoked with 900')
		self.changeVlan(900)

	def useCellRouter(self):
		logging.info('use cell router invoked...')
		logging.info('change vlan invoked with 902')
		self.changeVlan(902)


if (__name__ == '__main__'):
	util = SwitchUtil()
	util.useDefaultRouter()
