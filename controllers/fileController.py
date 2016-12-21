import csv
import os
from models.judgment import *
from pymodm import connect

# Connect to MongoDB and call the connection "my-app".
connect("mongodb://localhost:27017/crowdtruth", alias="default")

def processFile(root,directory,file):

	filename = root+directory+'/'+file

	job = file.split('.csv')[0]
	project = directory
	f = open(filename, 'r')
	reader = csv.DictReader(f)

	platform = getPlatform(reader)
	
	# add judgments in bulk
	judgments = []

	for row in reader:
		print project
		# get key values
		judgments.append(Judgment(
			id 		= platform+'/'+row['_id'],
			unit 	= platform+'/'+row['_unit_id'],
			worker 	= platform+'/'+row['_worker_id'],
			job		= job,
			platform = platform
#			channel	= row['_channel'],
#			country	= row['_country'],
#			region 	= row['_region'],
#			city 	= row['_city'],
#			ip 		= row['_ip']
		))

	Judgment.objects.bulk_create(judgments)


def getPlatform(reader):
	if reader.fieldnames[0] == '_unit_id':
		return 'cf'
	elif reader.fieldnames[0] == 'HITId':
		return 'amt'
	else:
		return False
	