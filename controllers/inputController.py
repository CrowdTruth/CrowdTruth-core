import os
from models import *
import sys  
# reload(sys)  
# sys.setdefaultencoding('utf8')
import chardet
#import Judgment, Worker, Unit, Job, Collection
class Found(Exception): pass
import re, string
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter, OrderedDict
import re
import groundtruthController as groundtruth
import pdb
import cProfile
import logging

pd.options.display.multi_sparse = False


# create an ordered counter so that we can maintain the position of tags in the order they were annotated
class OrderedCounter(Counter, OrderedDict):
	pass

def createOrderedCounter(orderedCounter, annotation_vector):
	for relation in annotation_vector:
		if relation not in orderedCounter:
			orderedCounter.update({relation: 0})
	return orderedCounter

# Connect to MongoDB and call the connection "my-app".


def processFile(root, directory, filename, config):

	job = filename.split('.csv')[0]

	#with open(root+'/'+directory+'/'+filename, 'rb') as f:
	#    result = chardet.detect(f.read())  # or readline if the file is large
	#    #print result['encoding']

	# judgments = pd.read_csv(root+'/'+directory+'/'+filename)#, encoding=result['encoding'])
	judgments = None
	
	if directory != "":
		logging.info("PROCESSING FOLDER: " + directory)
		files = os.listdir(directory)
		logging.info("FILE LIST: { " + ", ".join(files) + " }")
		for f in files:
		    f_data = pd.read_csv(root+"/"+directory + "/" + f, sep = config.column_separator)
		    
		    if judgments is None:
		    	judgments = f_data
		    else:
		      	judgments = judgments.append(f_data, ignore_index=True)
	else:
	  	judgments = pd.read_csv(filename, sep = config.column_separator)

#	if directory == '':
#		directory = '/'

	collection = directory

	platform = getPlatform(judgments)
	#print df.head()
	

	# we must establish which fields were part of the input data and which are output judgments
	# if there is a config, check if there is a definition of which fields to use
	#config = []
	# else use the default and select them automatically
	config = getColumnTypes(judgments, config)

	# remove rows where the worker did not give an answer (AMT issue)
	for col in config.outputColumns:
		judgments = judgments[pd.isnull(judgments[col]) == False]
	judgments = judgments.reset_index(drop=True)


	# allow customization of the judgments
	judgments = config.processJudgments(judgments)


	# update the config after the preprocessing of judgments
	config = getColumnTypes(judgments, config)
	
	allColumns = dict(config.input.items() + config.output.items() + platform.items())
	judgments = judgments.rename(columns=allColumns)

	# remove columns we don't care about
	judgments = judgments[allColumns.values()]

	judgments['job'] = job
	
	# print("COLUMNS WE WANT: " + " ".join(config.output.values()))
	
	#config.annotation_vector = [x.replace("per:", "") for x in config.annotation_vector]
	#config.annotation_vector = [x.replace("org:", "") for x in config.annotation_vector]
	
	#print judgments

	n_judgments = len(judgments)
	# make output values safe keys
	for col in config.output.values():
		if type(judgments[col].iloc[0]) is dict:
			# print("is dict")
			# print(judgments[col].iloc[0])
			if config.open_ended_task:
				judgments[col] = judgments[col].apply(lambda x: OrderedCounter(x))
			else:
				judgements[col] = judgements[col].apply(lambda x: createOrderedCounter(OrderedCounter(x), config.annotation_vector))	
		else:
			# print("is not dict")
			# print(judgments[col].iloc[0])
			#judgments[col] = judgments[col].apply(lambda x: OrderedCounter(x.split(",")))
			if config.open_ended_task:
				judgments[col] = judgments[col].apply(lambda x: OrderedCounter(x.split(config.annotation_separator)))
			else:
				judgments[col] = judgments[col].apply(lambda x: createOrderedCounter(OrderedCounter(x.split(config.annotation_separator)), config.annotation_vector))
		#print judgments[col]

		#if not config.open_ended_task:
		#	for idx in range(n_judgments):
		#		crnt_test_dict = test_dict[idx]
		#		for relation in config.annotation_vector:
					#print type(judgments[col][idx])
		#			if relation not in crnt_test_dict: #judgments[col][idx]:
						#judgments[col][idx].update({relation : 0})
		#				crnt_test_dict.update({relation: 0})


	#outputData = {config.output[col]:row[col] for col in config.output}
	
#	for col in config.output.values():
#		judgments['annotations.'+col] = judgments[col].apply(lambda x: getAnnotations(x))

	judgments['started'] = judgments['started'].apply(lambda x: pd.to_datetime(str(x)))
	judgments['submitted'] = judgments['submitted'].apply(lambda x: pd.to_datetime(str(x)))
	judgments['duration'] = judgments.apply(lambda row: (row['submitted'] - row['started']).seconds, axis=1)

	# 


	#
	# aggregate units
	#
	units = Unit.aggregate(judgments, config)


	#
	# compute worker agreement
	#
	for col in config.output.values():
	#	judgments[col+'.agreement'] = judgments.apply(lambda row: Worker.getUnitAgreement(row[col], units.at[row['unit'], col]), axis=1)	
		judgments[col+'.count'] = judgments[col].apply(lambda x: sum(x.values()))	
		#judgments[col+'.unique'] = judgments[col].apply(lambda x: len(x))	

	#judgments['worker-cosine'] = 1 - judgments.apply(lambda row: np.array([row[col+'.agreement'] for col in config.output.values()]).mean(), axis=1)

	#
	# aggregate workers
	#
	workers = Worker.aggregate(judgments, config)


	# get the thresholds
	#workerAgreementThreshold = workers['worker-agreement'].mean() - (2 * workers['worker-agreement'].std())
	#workerCosineThreshold = judgments['worker-cosine'].mean() + (2 * judgments['worker-cosine'].std())

	#
	# tag spammers
	#
	#workers['spam'] = (workers['worker-agreement'] < workerAgreementThreshold) & (workers['worker-cosine'] > workerCosineThreshold)
	#workers['spam'] = []


	# tag judgments that were spam
 	#judgments['spam'] = judgments['worker'].apply(lambda x: workers.at[x,'spam'])
 	# filteredJudgments = judgments[judgments['spam'] == False]
 	#filteredJudgments = judgments

	#
	# aggregate units
	#
	#units = Unit.aggregate(judgments, config)



	#
	# aggregate annotations
	# i.e. output columns
	#	
	annotations = pd.DataFrame()
	for col in config.output.values():
#		annotations[col] = pd.Series(judgments[col].sum())
		res = pd.DataFrame(judgments[col].apply(lambda x: pd.Series(x.keys()).value_counts()).sum(),columns=[col])
		annotations = pd.concat([annotations, res], axis=0)


	
	#
	# aggregate job
	#
	#job = Job.aggregate(units, filteredJudgments, workers, config)
	#job['spam'] = workers['spam'].sum() / float(workers['spam'].count())
	#job['spam.judgments'] = workers['spam'].sum()
	#job['spam.workers'] = workers['spam'].count()
	#job['workerAgreementThreshold'] = workerAgreementThreshold
	#job['workerCosineThreshold'] = workerCosineThreshold




	# Clean up judgments
	# remove input columns from judgments
	outputCol = [col for col in judgments.columns.values if col.startswith('output') or col.startswith('metric')]
	judgments = judgments[outputCol + platform.values() + ['duration','job']]
	
	# set judgment id as index
	judgments.set_index('judgment', inplace=True)

	# measure performance with ground truth
	#job, units = groundtruth.process(job, units.copy(), config.groundtruth)

	#print(units)
        #print("\n\n\n\n\n")
	# add missing vector values if closed task
	for col in config.output.values():
		if not config.open_ended_task:
		    for idx in list(units.index):
		        for relation in config.annotation_vector:
		            if relation not in units[col][idx]:
		                units[col][idx].update({relation : 0})
        #print(units)
        #return
	return {
	#	'jobs' : job, 
		'units' : units,
		'workers' : workers,
		'judgments' : judgments,
		'annotations' : annotations
		}



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
			config.input = {c:'input.'+c.replace('Input.','') for c in df.columns.values if c in config.inputColumns}
		else:
			config.input = {c:'input.'+c.replace('Input.','') for c in df.columns.values if c.startswith('Input.')}
		
		# if config is specified, use those columns
		if config.outputColumns:
			config.output = {c:'output.'+c.replace('Answer.','') for c in df.columns.values if c in config.outputColumns}
		else:
			config.output = {c:'output.'+c.replace('Answer.','') for c in df.columns.values if c.startswith('Answer.')}
		return config

	elif df.columns.values[0] == '_unit_id':
		# returns a list of columns that contain are input content
		config.input = {}
		config.output = {}

		# if a config is specified, use those columns
		if config.inputColumns:
			config.input = {c:'input.'+c for c in df.columns.values if c in config.inputColumns}
		if config.outputColumns:
			config.output = {c:'output.'+c for c in df.columns.values if c in config.outputColumns}
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
				if not config.inputColumns:
					config.input[c] = 'input.'+c

			except Found:
				if not config.outputColumns:
					config.output[c] = 'output.'+c
#				print 'output:',c

		return config
	else:
		# unknown platform type
		return config	

def getAnnotations(field, config = []):
	return OrderedCounter(getSafeKey(str(field)))


# turn values into safe mongo keys
def getSafeKey(field):
	pattern = re.compile('(?!,)[\W_]+')
	cleanField = re.sub(' +',' ', field.replace('"','').lower().strip())
	# see if the string is an array
	fields = map(lambda x: pattern.sub(' ', x).strip().replace(' ', '_'), re.split(',|\|',cleanField))
	
	fields = [f for f in fields if len(f) > 0]
	
	if len(fields):
		return fields
	else:
		return ['__None__']
