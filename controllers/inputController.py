import os
from models import *
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
#import Judgment, Worker, Unit, Job, Collection
class Found(Exception): pass
import re, string
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

pd.options.display.multi_sparse = False

# Connect to MongoDB and call the connection "my-app".

def processFile(root, directory, filename):

	job = filename.split('.csv')[0]

	judgments = pd.read_csv(root+'/'+directory+'/'+filename)

	if directory == '':
		directory = '/'

	collection = directory


	platform = getPlatform(judgments)
	#print df.head()
	


	# track units so that we do not have to add the unit specific variables on each row iteration
	prevUnit = 0

	# we must establish which fields were part of the input data and which are output judgments
	# if there is a config, check if there is a definition of which fields to use
	#config = []
	# else use the default and select them automatically
	inputColumns, outputColumns = getColumnTypes(judgments)

	allColumns = dict(inputColumns.items() + outputColumns.items() + platform.items())
	judgments = judgments.rename(columns=allColumns)

	# remove columns we don't care about
	judgments = judgments[allColumns.values()]

	judgments['job'] = job

	# make output values safe keys
	for col in outputColumns.values():
		judgments[col] = judgments[col].apply(lambda x: getSafeKey(str(x)))

	#outputData = {outputColumns[col]:row[col] for col in outputColumns}
	
#	for col in outputColumns.values():
#		judgments['annotations.'+col] = judgments[col].apply(lambda x: getAnnotations(x))

	judgments['started'] = judgments['started'].apply(lambda x: pd.to_datetime(x))
	judgments['submitted'] = judgments['submitted'].apply(lambda x: pd.to_datetime(x))
	judgments['duration'] = judgments.apply(lambda row: (row['submitted'] - row['started']).seconds, axis=1)




	#
	# aggregate units
	#
	agg = {}
	for col in inputColumns.values():
		# for each input column the first value is taken. all rows have the same value for each unit.
		agg[col] = 'first'
	for col in outputColumns.values():
		# each output column dict is summed
		agg[col] = lambda x: dict(Counter(x))
	agg['job'] = 'first'
	agg['worker'] = 'count'
	agg['duration'] = 'mean'

	units = judgments.groupby('unit').agg(agg)

	# get unit metrics
	for col in outputColumns.values():
		# for each vector in the unit get the unit metrics
		units[col+'.metrics'] = units[col].apply(lambda x: Unit.getUnitMetrics(x))
	metrics = units[outputColumns.values()[0]+'.metrics'].iloc[0].keys()
	# aggregate unit metrics
	for val in metrics:
		units['metrics.avg_'+val] = units.apply(lambda row: np.mean([row[x+'.metrics'][val] for x in outputColumns.values()]), axis=1)

	units = units.reindex_axis(sorted(units.columns), axis=1)


	# compute worker agreement
	for col in outputColumns.values():
		judgments[col+'.agreement'] = judgments.apply(lambda row: Unit.getVectorAgreement(dict(Counter([row[col]])), units.loc[row['unit'], col]), axis=1)	
	judgments['metrics_avg_agreement'] = judgments.apply(lambda row: np.array([row[col+'.agreement'] for col in outputColumns.values()]).mean(), axis=1)

	#
	# aggregate workers
	#
	agg = {}
	for col in outputColumns.values():
		# each output column dict is summed
		agg[col] = lambda x: dict(Counter(x))

	workers = judgments.groupby('worker').agg({
		'job' : 'nunique',
		'unit' : 'count',
		'judgment' : 'count',
		'duration' : 'mean',
		'metrics_avg_agreement' : 'mean'
		})



	#
	# aggregate annotations
	# i.e. output columns
	#
	annotations = pd.DataFrame()
	for col in outputColumns.values():
		annotations[col] = judgments[col].value_counts()



	# aggregate collection
	# TODO: move to main class
	collections = pd.DataFrame(columns = ['id'])
	collections.loc[collection] = {'id' : directory}

	# aggregate job
	jobs = pd.DataFrame(columns = ['collection', 'filename'])#, 'platform'])
	jobs.loc[job] = {'collection' : collection, 'job' : job}#, 'platform' : platform['_platform']}

	job = judgments.groupby('job').agg({
		'unit' : 'nunique',
		'judgment' : 'count',
		'worker' : 'nunique',
		'duration' : 'mean',
		'metrics_avg_agreement' : 'mean'
		})


	outputCol = [col for col in judgments.columns.values if col.startswith('output') or col.startswith('metric')]
	# remove input columns
	judgments = judgments[outputCol + platform.values() + ['duration']]

	# set judgment id as index
	judgments.set_index('judgment', inplace=True)


	return {
		'jobs' : job, 
		'units' : units,
		'workers' : workers,
		'judgments' : judgments,
		'annotations' : annotations
		}

	'''
	#j.process(judgments, workers, units)
	'''




def getPlatform(df):
	# Get the crowdsourcing platform this file originates to

	if df.columns.values[0] == '_unit_id':
		# CrowdFlower
		return {
			#'_platform'		: 'cf',
			'_id' 			: 'judgment',
			'_unit_id' 		: 'unit',
			'_worker_id' 	: 'worker',
			'_started_at'	: 'started',
			'_created_at'	: 'submitted'
		}
	elif df.columns.values[0] == 'HITId':
		# Mturk
		return {
			#'id'		: 'amt',
			'AssignmentId' 	: 'judgment',
			'HITId' 		: 'unit',
			'WorkerId' 		: 'worker',
			'AcceptTime'	: 'started',
			'SubmitTime'	: 'submitted'
		}
	else:
		# Not supported
		return False



def getColumnTypes(df):
	# get a dict of the columns with input content and the columns with output judgments
	# each entry matches [original column name]:[safestring column name]

	if df.columns.values[0] == 'HITId':
		# Mturk
		inputColumns = {c:'input.'+c.replace('Input.','') for c in df.columns.values if c.startswith('Input.')}
		outputColumns = {c:'output.'+c.replace('Answer.','') for c in df.columns.values if c.startswith('Answer.')}
		return inputColumns, outputColumns
	elif df.columns.values[0] == '_unit_id':
		# returns a list of columns that contain are input content
		# this is the case if all the values in the column are identical
		# this is not failsafe but should give decent results without settings
		# it is best to make a settings.ini file for a collection
		inputColumns = {}
		outputColumns = {}


		# analyse the first unit only
		unit = df.loc[df['_unit_id'] == df['_unit_id'][0]]
		units = df.groupby('_unit_id')

		columns = [c for c in unit.columns.values if not c.startswith('_') and not c.endswith('_gold') and not c.endswith('_reason') and not c.endswith('browser')]
		for c in columns:

			try:
				for i, unit in units:
					if unit[c].nunique() <> 1:
						raise Found
#				print 'input:',c
				inputColumns[c] = 'input.'+c

			except Found:
				outputColumns[c] = 'output.'+c
#				print 'output:',c

		return inputColumns, outputColumns
	else:
		# unknown platform type
		return [], []		

def getAnnotations(field, config = []):
	# use config to make the vector
	if len(config) > 0:
		return {}
	# if no config just aggregate the values
	else:
		return {getSafeKey(field):1}


# turn values into safe mongo keys
def getSafeKey(field):
	pattern = re.compile('[\W_]+')
	safe = pattern.sub('_', field)
	return safe