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

with open ('names.txt', 'r') as f:
	names = f.readlines()
	names = list(map(lambda s: s.rstrip(), names))

import random

def random_rating():
	return min(5.00, random.gauss(3.75, 0.8))

tags = [
	'Good at explaining things',
	'Expert in their field',
	'Is friendly',
	'Fun lessons',
	'Practical examples',
	'Good notes',
	'Enthusiastic',
	'Sets clear, achievable goals',
	'Prepared and organised',
	'Gives me work appropriate for my ability',
	'Makes efficient use of tutorial time',
	'Gives great feedback',
	'Tailored lessons',
	'Sets challenging work'
]

areas = [
	'Front-end',
	'Back-end',
	'iOS',
	'Android',
	'Security',
	'Machine Learning'
]

def random_tag_scores():
	return {tag: random_rating() for tag in tags}

def random_areas():
	return random.sample(areas, random.randint(2, 4))

def insert_instructor(name, tag_scores, _areas, academic):
	email = '.'.join(name.lower().split(' ')) + '@' + random.choice(['gmail.com', 'outlook.com', 'live.com']) 
	db['instructors'].insert_one({'name': name, 'tag-scores': tag_scores, 'areas': _areas, 'email': email})

for name in names:
	insert_instructor(name, random_tag_scores(), random_areas(), bool(random.randint(0, 1)))
