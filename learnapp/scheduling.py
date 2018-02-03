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
		response = requests.post(destination, headers=headers, auth=auth, data=data)
		return response.json()

if __name__ == '__main__':
	data = {
		'name': 'Patrick Hainge',
		'timezone': 'Europe/London',
		'email': 'patrick.hainge@outlook.co.uk',
		'password': 'hunter2'
	}
	print(create_resource(json.dumps(data)))