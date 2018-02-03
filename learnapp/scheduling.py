import datetime
import json
import requests

from requests.auth import HTTPBasicAuth

def timestamp():
	return datetime.datetime.now().isoformat() # timestamp for findtime

auth = HTTPBasicAuth('', 'live_api_key_tXXMZt6VzWrTf1uhuPfQqb5WN57j9KN2')

api = 'https://api.timekit.io/v2'

uid = '084d6514-cd1d-432f-87f5-9c40c0d359fd'

headers = {'content-type': 'application/json'}

def get_resource(uid):
	destination = '/'.join((api, 'resources', uid+'?includes=calendars'))
	response = requests.get(destination, headers=headers, auth=auth)
	return response.json()

def find_time(data):
	"""
	data = {
		'resource_ids': [],
		'filters': {},
		'future': '2 days',
		'length': '30 minutes'
	}
	"""
	destination = '/'.join((api, 'findtime'))
	response = requests.post(destination, headers=headers, auth=auth, data=json.dumps(data))
	return response.json()

def create_resource(data):
	"""
	data = {
		'name': '',
		'timezone': '',
		'email': '',
		'password': 
	}
	"""
	if not all(key in data for key in {'name', 'timezone'}):
		return None
	else:
		destination = api + '/resources'
		response = requests.post(destination, headers=headers, auth=auth, data=json.dumps(data))
		return response.json()

def book(data):
	"""
	data'{
    "resource_id": {id},
    "graph": "confirm_decline",
    "start": "2015-03-01T08:00:00+00:00",
    "end": "2015-03-01T13:00:00+00:00",
    "what": "A would like to book the DeLorean",
    "where": "Sesame St, Middleburg, FL 32068, USA",
    "description": "Please arrive 10 minutes before you time begin",
    "customer": {
      "name": "Marty McFly",
      "email": "marty.mcfly@timekit.io",
      "phone": "1-591-001-5403",
      "voip": "McFly",
      "timezone": "America/Los_Angeles"
    }
	"""
	destination = api + '/bookings'
	response = requests.post(destination, headers=headers, auth=auth, data=json.dumps(data))
	return response.json()

if __name__ == '__main__':
	data = {
		'name': 'Hatrick Painge',
		'email': 'patrick.hainge@outlook.com',
		'timezone': 'Europe/London',
		'password': 'hunter2'
	}
	print(create_resource(data))