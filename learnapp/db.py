from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://root:root@ds113455.mlab.com:13455/fb-hack')
import random
db = client['fb-hack']

def weight_sum(tag_weights, tags):
	ret = sum(tags[tag] * weight for tag, weight in tag_weights.items())
	return ret

def score(tags, areas, instructor):
	tag_weights = weight_sum(tags, instructor.get('tag-scores'))
	areas = set(areas)
	instructor_areas = set(instructor.get('areas'))
	overlap = len(areas.intersection(instructor_areas)) / len(areas.union(instructor_areas))
	return 0.6 * tag_weights + 0.4 * overlap

def get_matches_for(email):

	student = db['students'].find_one({'email': email})
	tags = student['tag-weights']
	areas = student['areas']

	area_matches = list(db['instructors'].find({'areas': {'$in': areas}}))
	scores = list(map(lambda i: score(tags, areas, i), area_matches))
	m = max(scores)
	scores = list(map(lambda s: 100 * (s / m), scores))
	area_matches = [(i, '%.2f' % s) for s, i in sorted(zip(scores, area_matches), reverse=True)]
	for i, match in enumerate(area_matches):
		match[0]['class'] = 'pane' + str(i+1)
		match[0]['img'] = 'https://randomuser.me/api/portraits/' + random.choice(['men', 'women']) + '/' + str(i) + '.jpg'
		match[0]['id'] = str(match[0]['_id'])
		match[0]['tag_scores'] = match[0]['tag-scores']
		del match[0]['tag-scores']
	return area_matches[:5]

def get_matches(skills):
	ret = find_instructors_for(skills)
	sorted(ret, key=lambda i: len(set(skills).intersection(set(i.get('skills')))))
	return ret

def find_instructors_for(skills):
	return list(db['instructors'].find({'skills': {'$in': skills}}))

def get_instructor(id):
	ret = db['instructors'].find_one({'_id': ObjectId(id)})
	scores = ret['tag-scores']
	for k, v in scores.items():
		scores[k] = "%.2f" % (100.0 * (v / 5.0)) + "%"
		print(scores[k])
	del ret['tag-scores']
	ret['tag_scores'] = scores
	return ret

def set_availability(uid, data):
	db['students'].update_one(
		{'_id': ObjectId(uid)},
		{'$set':
			{
				'availability': data
			}
		},
		upsert=False
	)

def availability_filters(uid):
	student = db['students'].find_one({'_id': ObjectId(uid)})
	availability = student['availability']
	filters = {"or": list()}
	for k, v in availability.items():
		filters['or'].append({"specific_day_and_time": {"day": k, "start": v['start'], "end": v['end'], 'timezone': 'Europe/London'}})
	return filters

def pool(course, module):
	course = db['requests'].find_one({'course': ObjectId(course)})
	module = course['modules'][module]
	oids = list(module)
	emails = list(map(lambda oid: db['students'].find_one({'_id': ObjectId(oid)})['email'], oids))
	return emails

def avg_completion_time(course):
	def f(x):
		return 1 / (x/10) if x != 0 else 5
	return list(map(lambda n: (n, f(n)), range(0,105,5)))

def completion_likelihood(course):
	import random
	n = random.randint(75, 99)
	return 0.01 * n

if __name__ == '__main__':
	#print(get_matches(['python', 'haskell']))
	#print(pool('5a75e2de734d1d3bd58c804e', 'Map, filter, and reduce'))
	print(get_matches_for('patrick.hainge@kcl.ac.uk')[:1])



