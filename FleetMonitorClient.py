import os
import urllib
import urllib2
import datetime
import utils

'''
Utility to interact with fleetmonitor web service
'''
class FleetMonitorClient():
	def __init__(self):
		self.__baseUrl = str(os.environ['BINARY_CHECK_IN_URL'])

	@property
	def baseUrl(self):
	    return self._baseUrl

	def postCheckIn(self, status):
		checkInUrl = self.__baseUrl + '/check_ins'

		# TODO: consider dynamically access mac address (device id)
		# as opposed to storing in environment
		deviceId = str(os.environ['BINARY_DEVICE_ID'])
		time = str(datetime.datetime.now())
		monitoringVersion = str(utils.monitoringVersion())
		osVersion = utils.kernelVersion()

		values = dict(device_id = deviceId, monitoring_version = monitoringVersion,
			os_version = osVersion, primary_status = status, cell_status = status,
			check_in_time = time)
		data = urllib.urlencode(values)
		request = urllib2.Request(checkInUrl, data)

		# TODO: wrap this request with a fail handler -> write to local storage
		response = urllib2.urlopen(request)
		content = response.read()
