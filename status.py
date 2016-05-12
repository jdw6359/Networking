import urllib
import urllib2
import datetime

BASE_URL = 'http://localhost:3000'

print 'making the GET request...'

# Make a GET request
clientUrl = BASE_URL + '/clients'
request = urllib2.Request(clientUrl)
response = urllib2.urlopen(request)
content = response.read()

print 'done making GET request...'
print 'making the POST request...'

deviceId = 'UMZUWcIgGbi9T_oOd5M1a9Ozo1lhVdVHrs-I5Ga1pyMVWiBsvY1CU42SQ4hc1icP'
monitorUrl = BASE_URL + '/check_ins'

time = str(datetime.datetime.now())
status = "UP"

values = dict(device_id=str(deviceId), status=status, check_in_time=time)
data = urllib.urlencode(values)
request = urllib2.Request(monitorUrl, data)
response = urllib2.urlopen(request)
content = response.read()

print 'content: ' + str(content)
print 'done making POST request'
