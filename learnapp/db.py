from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://root:root@ds113455.mlab.com:13455/fb-hack')

db = client['fb-hack']

def get_matches(skills):
	ret = find_instructors_for(skills)
	sorted(ret, key=lambda i: len(set(skills).intersection(set(i.get('skills')))))
	return ret

def get_instructors():
	return list(db['instructors'].find())

def get_instructor(email):
	return db['instructors'].find_one({'email': email})

def find_instructors_for(skills):
	return list(db['instructors'].find({'skills': {'$in': skills}}))

def pool(course, module):
	course = db['requests'].find_one({'course': ObjectId(course)})
	module = course['modules'][module]
	return list(module)

def avg_completion_time(course):
	def f(x):
		from math import e as e_const
		return 1 / (1 + (e_const**-(-4+0.1*x)))
	return list(map(lambda n: (n, f(n)), range(0,100,10)))

def get_availability(uid):
	pass

def find_common_availability(students):
	"""
	24 * 7 1hr buckets, add every available time for every student
	sort by length of value list
	return max 3 as suggestions
	"""
	pass

if __name__ == '__main__':
	#print(get_matches(['python', 'haskell']))
	#print(pool('5a75e2de734d1d3bd58c804e', 'Map, filter, and reduce'))
	print(avg_completion_time('a'))