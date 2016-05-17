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

		# TODO: consider dynamically accessing mac address (device id)
		# as opposed to storing in environment
		deviceId = str(os.environ['BINARY_DEVICE_ID'])
		time = str(datetime.datetime.now())
		monitoringVersion = str(utils.monitoringVersion())
		osVersion = utils.kernelVersion()

		values = dict(device_id = deviceId, monitoring_version = monitoringVersion,
			os_version = osVersion, status = status, check_in_time = time)
		data = urllib.urlencode(values)
		request = urllib2.Request(checkInUrl, data)

		try:
			response = urllib2.urlopen(request)
			content = response.read()
		except urllib2.URLError:
			# TODO: write a fatal log message
			pass

	def postDowntimeSegment(self, startTime, endTime, bytesTraffic):
		downtimeSegmentUrl = self.__baseUrl + '/downtime_segments'

		# TODO: consider dynamically accessing mac address (device id)
		# as opposed to storing in environment
		deviceId = str(os.environ['BINARY_DEVICE_ID'])

		values = dict(device_id = deviceId, start_time = startTime, end_time = endTime,
			bytes_traffic = bytesTraffic)
		data = urllib.urlencode(values)
		request = urllib2.Request(downtimeSegmentUrl, data)

		try:
			response = urllib2.urlopen(request)
			content = response.read()
		except urllib2.URLError:
			# TODO: write a fatal log message
			pass