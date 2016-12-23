import os
from models.entities import *
from pymodm import connect
import re, string
import pandas as pd
from datetime import datetime

# Connect to MongoDB and call the connection "my-app".
connect("mongodb://localhost:27017/crowdtruth", alias="default")

def processFile(root,directory,file):

	filename = root+directory+'/'+file

	job = file.split('.csv')[0]
	existing = Job.objects.raw({'_id': job}).count()

	if existing > 10:
		return False

	project = directory
	df = pd.read_csv(filename)

	platform = getPlatform(df)
	collection = directory

	Collection(collection).save()
	#print Collection.objects.comment_counts()
	Job(job, collection, platform).save()
	
	# add judgments in bulk
	judgments = []
	units = {}
	workers = {}

	# we must establish which fields were part of the input data and which are output judgments
	# if there is a config, check if there is a definition of which fields to use
	#config = []
	# else use the default and select them automatically
	inputColumns, outputColumns = getColumnTypes(df)

	for index, row in df.iterrows():
		# get key values
		judgment = platform['id']+'/'+str(row[platform['judgment']])
		unit = platform['id']+'/'+str(row[platform['unit']])
		worker = platform['id']+'/'+str(row[platform['worker']])
		
		inputData = {col:row[col] for col in inputColumns}
		outputData = {col:row[col] for col in outputColumns}
		annotationVector = getAnnotationVector(outputData)

		if unit not in units:
			units[unit] = {
				'_id'			: unit,
				'collection' 	: collection,
				'job'			: job,
				'platform'		: platform['id'],
				'content'		: inputData
			}

		if worker not in workers:
			workers[worker] = {
				'_id'		: worker,
				'platform' 	: platform['id']
			}
	#			channel	= row['_channel'],
	#			country	= row['_country'],
	#			region 	= row['_region'],
	#			city 	= row['_city'],
	#			ip 		= row['_ip']


		started = datetime.strptime(row[platform['started']], platform['timeformat'])
		submitted = datetime.strptime(row[platform['submitted']], platform['timeformat'])
		duration = (submitted - started).total_seconds()

		judgments.append(Judgment(
			judgment,
			collection,
			job,
			unit,
			worker,
			platform['id'],
			outputData,
			annotationVector,
			started,
			submitted,
			duration
		))

	Judgment.objects.bulk_create(judgments)

	# create or update the workers
	for worker in workers:
		w = Worker().from_document(workers[worker])
		w.getFeatures()
		w.save()

	# create or update the units
	for unit in units:
		u = Unit().from_document(units[unit])
		u.getFeatures()
		u.save()



def getPlatform(df):
	# Get the crowdsourcing platform this file originates to

	if df.columns.values[0] == '_unit_id':
		# CrowdFlower
		return {
			'id'		: 'cf',
			'judgment' 	: '_id',
			'unit' 		: '_unit_id',
			'worker' 	: '_worker_id',
			'started'	: '_started_at',
			'submitted'	: '_created_at',
			'timeformat' : "%m/%d/%Y %H:%M:%S"
		}
	elif df.columns.values[0] == 'HITId':
		# Mturk
		return {
			'id'		: 'amt',
			'judgment' 	: 'AssignmentId',
			'unit' 		: 'HITId',
			'worker' 	: 'WorkerId',
			'started'	: 'AcceptTime',
			'submitted'	: 'SubmitTime',
			'timeformat' : "%a %b %d %H:%M:%S %Z %Y"
		}
	else:
		# Not supported
		return False



def getColumnTypes(df):
	# get a list of the columns with input content and the columns with output judgments

	if df.columns.values[0] == 'HITId':
		# Mturk
		inputColumms = [c for c in df.columns.values if not c.startswith('_') and not c.endswith('_gold')]
		outputColumns = []
		return inputColumns, outputColumns
	elif df.columns.values[0] == '_unit_id':
		# returns a list of columns that contain are input content
		# this is the case if all the values in the column are identical
		# this is not failsafe but should give decent results without settings
		# it is best to make a settings.ini file for a collection
		inputColumns = []
		outputColumns = []

		# analyse the first unit only
		unit = df.loc[df['_unit_id'] == df['_unit_id'][0]]

		columns = [c for c in unit.columns.values if not c.startswith('_') and not c.endswith('_gold')]
		for c in columns:
			if(len(set(unit[c])) <= 1):
				inputColumns.append(c)
			else:
				outputColumns.append(c)
		return inputColumns, outputColumns
	else:
		# unknown platform type
		return [], []		

def getAnnotationVector(content, config = []):
	# use config to make the vector
	if len(config) > 0:
		return {}
	# if no config just aggregate the values
	else:
		return {field: {getSafeKey(content[field]):1} for field in content}


# turn values into safe mongo keys
def getSafeKey(field):
	pattern = re.compile('[\W_]+')
	safe = pattern.sub('', field)
	return safe