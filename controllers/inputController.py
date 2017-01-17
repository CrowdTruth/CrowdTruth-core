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
import re
pd.options.display.multi_sparse = False

# Connect to MongoDB and call the connection "my-app".

def progress(job_title, progress):
	length = 10 # modify this to change the length
	block = int(round(length*progress))
	msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100))
	if progress >= 1: msg += " DONE\r\n"
	sys.stdout.write(msg)
	sys.stdout.flush()


def processFile(root, directory, filename, config):

	progress(filename,0.1)
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
	config = getColumnTypes(judgments, config)

	allColumns = dict(config.input.items() + config.output.items() + platform.items())
	judgments = judgments.rename(columns=allColumns)

	# remove columns we don't care about
	judgments = judgments[allColumns.values()]

	judgments['job'] = job

	annotations = judgments.loc[:,config.output.values()+['judgment']]

	progress(filename,.3)

	# make output values safe keys
	for col in config.output.values():
		judgments[col] = judgments[col].apply(lambda x: Counter(getSafeKey(str(x))))

	#outputData = {config.output[col]:row[col] for col in config.output}
	
#	for col in config.output.values():
#		judgments['annotations.'+col] = judgments[col].apply(lambda x: getAnnotations(x))

	judgments['started'] = judgments['started'].apply(lambda x: pd.to_datetime(x))
	judgments['submitted'] = judgments['submitted'].apply(lambda x: pd.to_datetime(x))
	judgments['duration'] = judgments.apply(lambda row: (row['submitted'] - row['started']).seconds, axis=1)


	progress(filename,.5)



	#
	# aggregate units
	#
	units = Unit.aggregate(judgments, config)
	progress(filename,.6)


	#
	# compute worker agreement
	#
	for col in config.output.values():
		judgments[col+'.agreement'] = judgments.apply(lambda row: Worker.getUnitAgreement(row[col], units.loc[row['unit'], col]), axis=1)	
	judgments['metrics.worker.agreement'] = judgments.apply(lambda row: np.array([row[col+'.agreement'] for col in config.output.values()]).mean(), axis=1)

	progress(filename,.8)



	#
	# aggregate workers
	#

	workers = judgments.groupby('worker')

	#workerAgreement = Worker.getAvgWorkerAgreement(workers)
	#print workerAgreement.head()

	workers = workers.agg({
		'job' : 'nunique',
		'unit' : 'count',
		'judgment' : 'count',
		'duration' : 'mean',
		'metrics.worker.agreement' : 'mean'
		})

	#workerAgreement = Worker.getAvgWorkerAgreement(workers)



	#
	# aggregate annotations
	# i.e. output columns
	#
	'''
	annotations = pd.DataFrame()
	for col in config.output.values():
		#print units[col].values
		annotations[col] = judgments[col].apply(lambda x: pd.Series(x.keys()).value_counts()).sum()
	'''


	# aggregate collection
	# TODO: move to main class
	collections = pd.DataFrame(columns = ['id'])
	collections.loc[collection] = {'id' : directory}

	# aggregate job
	jobs = pd.DataFrame(columns = ['collection', 'filename'])#, 'platform'])
	jobs.loc[job] = {'collection' : collection, 'job' : job}#, 'platform' : platform['_platform']}


	# each output column dict is summed
	agg = {x+'.agreement' : 'mean'  for x in config.output.values()}
	agg.update({
		'unit' : 'nunique',
		'judgment' : 'count',
		'worker' : 'nunique',
		'duration' : 'mean',
		'metrics.worker.agreement' : 'mean'
	})
	job = judgments.groupby('job').agg(agg)


	for val in config.output.values():
		job[val+'.agreement'] = np.mean(units.apply(lambda row: row[val+'.metrics']['max_relation_Cos'], axis=1))
#	print job['output.debated.agreement']



	# add unit metrics to job metrics
	metrics = units[config.output.values()[0]+'.metrics'].iloc[0].keys()
	for val in metrics:
		job['metrics.unit.avg_'+val] = units['metrics.avg_'+val].mean()


	# compute job runtime
	runtime = (max(judgments['submitted']) - min(judgments['started']))
	job['runtime'] = float(runtime.days) * 24 + float(runtime.seconds) / 3600
	job['judgments.per.worker'] = job['judgment'] / job['worker']



	outputCol = [col for col in judgments.columns.values if col.startswith('output') or col.startswith('metric')]
	# remove input columns
	judgments = judgments[outputCol + platform.values() + ['duration']]

	# set judgment id as index
	judgments.set_index('judgment', inplace=True)




	progress(filename,1)

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



def getColumnTypes(df, config):
	# get a dict of the columns with input content and the columns with output judgments
	# each entry matches [original column name]:[safestring column name]

	if df.columns.values[0] == 'HITId':
		# Mturk
		# if config is specified, use those columns
		if config.inputColumns:
			config.input = {c:'input.'+c.replace('Input.','') for c in config.inputColumns}
		else:
			config.input = {c:'input.'+c.replace('Input.','') for c in df.columns.values if c.startswith('Input.')}
		
		# if config is specified, use those columns
		if config.outputColumns:
			config.output = {c:'output.'+c.replace('Answer.','') for c in config.outputColumns}
		else:
			config.output = {c:'output.'+c.replace('Answer.','') for c in df.columns.values if c.startswith('Answer.')}
		return config

	elif df.columns.values[0] == '_unit_id':
		# returns a list of columns that contain are input content
		config.input = {}
		config.output = {}

		# if a config is specified, use those columns
		if config.inputColumns:
			config.input = {c:'input.'+c for c in config.inputColumns}
		if config.outputColumns:
			config.output = {c:'output.'+c for c in config.outputColumns}

		# if there is a config for both input and output columns, we can return those
		if config.inputColumns and config.outputColumns:
			return config

		# try to identify the input and output columns
		# this is the case if all the values in the column are identical
		# this is not failsafe but should give decent results without settings
		# it is best to make a settings.py file for a collection

		units = df.groupby('_unit_id')
		columns = [c for c in df.columns.values if c <> 'clustering' and not c.startswith('_') and not c.startswith('e_') and not c.endswith('_gold') and not c.endswith('_reason') and not c.endswith('browser')]
		for c in columns:
#			if df[c].nunique() == 1:
				# ignore the column if all values are the same
#				continue
			try:
				for i, unit in units:
					unique = unit[c].nunique()
					if unique <> 1 and unique <> 0:
						raise Found
#				print 'input:',c
				if not inputColumns:
					config.input[c] = 'input.'+c

			except Found:
				if not outputColumns:
					config.output[c] = 'output.'+c
#				print 'output:',c

		return config
	else:
		# unknown platform type
		return config	

def getAnnotations(field, config = []):
	# use config to make the vector
	if len(config) > 0:
		return {}
	# if no config just aggregate the values
	else:
		return {getSafeKey(field):1}


# turn values into safe mongo keys
def getSafeKey(field):
	pattern = re.compile('(?!,)[\W_]+')
	cleanField = re.sub(' +',' ', str(field).lower())
	fields = map(lambda x: pattern.sub('_', x.strip()), re.split(',|\|',cleanField))
	fields = [f for f in fields if len(f) > 0]
	return fields