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

def find_time(uid, data):
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
		'resource_id': 'e9759786-416d-4a80-af64-4c48a7c615e1',
		'graph': 'confirm_decline',
		'start': '2018-02-04T15:00:00+00:00',
		'end': '2018-02-04T16:00:00+00:00',
		'what': 'Tutorial on lambdas in Python',
		'where': 'Online',
		'description': '',
		'customer': {
			'name': 'Test Customer',
			'email': 'haingep@gmail.com',
			'timezone': 'Europe/London'
		}
	}
	print(book(data))