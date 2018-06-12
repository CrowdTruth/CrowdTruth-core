import os

from models.metrics import *
from models.worker import *
from models.unit import *
from models.job import *
from configuration import DefaultConfig

import logging
import pdb

import sys  
#reload(sys)  
#sys.setdefaultencoding('utf8')
import chardet
#import Judgment, Worker, Unit, Job, Collection
import re, string
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter, OrderedDict
import re
#import groundtruthController as groundtruth
#pd.options.display.multi_sparse = False


# create an ordered counter so that we can maintain the position of tags in the order they were annotated
class OrderedCounter(Counter, OrderedDict):
	pass

def createOrderedCounter(orderedCounter, annotation_vector):
	for relation in annotation_vector:
		if relation not in orderedCounter:
			orderedCounter.update({relation: 0})
	return orderedCounter


class Found(Exception): pass


def progress(job_title, progress):
	length = 10 # modify this to change the length
	block = int(round(length*progress))
	msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100))
	if progress >= 1: msg += " DONE\r\n"
	# sys.stdout.write(msg)
	# sys.stdout.flush()
	# logging.info(msg)

def getFileList(directory):
	filelist = []

	# go through all files in this folder
	for f in os.listdir(directory):
		# if it is a folder scan it
		if os.path.isdir(directory+'/'+f):
			sublist = getFileList(directory+'/'+f)
			if len(sublist):
				filelist.append(sublist)

		# if it is a csv file open it
		elif f.endswith('.csv') and f <> 'groundtruth.csv':
			filelist.append(f)
	return filelist

def load(**kwargs):


	# placeholder for aggregated results
	results = {
		#'collections' : {},
		'jobs' : [],
		'units' : [],
		'workers' : [],
		'judgments' : [],
		'annotations' : []
		}


	if 'config' not in kwargs:
		config = DefaultConfig()
	else:
		logging.info('Config loaded')
		config = kwargs['config']

	# check if files is a single file or folder
	if('file' in kwargs and kwargs['file'].endswith('.csv')):
		files = [kwargs['file']]
	elif('directory' in kwargs):
		directory = kwargs['directory']
		files = getFileList(directory)
		logging.info('Found ' + str(len(files)) + ' files')
	else:
		raise ValueError('No input was provided')


	for f in files:
		if 'directory' in locals():
			logging.info("Processing " + f)
			f = directory+f
		res, config = processFile(f, config)
		for x in res:
			results[x].append(res[x])


	for x in results:
		results[x] = pd.concat(results[x])


	# workers and annotations can appear across jobs, so we have to aggregate those extra
	results['workers'] = results['workers'].groupby(results['workers'].index).agg({
		'unit' : 'sum',
		'judgment' : 'sum',
		'job' : 'count',
		'duration' : 'mean'
		#'spam' : 'sum',
		#'worker-cosine' : 'mean',
		#'worker-agreement' : 'mean'
		})



	# aggregate annotations
	results['annotations'] = results['annotations'].groupby(results['annotations'].index).sum()
	

	#
	# compute correlations
	#
	# remove 'output.' from the annotation column names
	

	# How many times person a meets person b is described by the following (s.t. a < b)


	# DataFrames corr() function calculates pairwise correlations using specified 
	# algorithm: 'peason, 'kendall', and 'spearman' are supported.
	# Correlations are returned in a new DataFrame instance (corr_df below).
	#likert_corr_df = likert.corr(method='pearson')
	#likert_corr_df.to_csv(wd+'/results/likert_correlations.csv', sep=',')

	# CT metrics 2.0
	#results = Metrics.run(results, config)

	# add customized results
#	for c in config.output.items():
#		results['units'][c[1]] = results['units'][c[1]].apply(lambda x: dict(x))

	# clean up judgments
#	for col in config.output.values():
		#print col
		#results['judgments'][col] = results['judgments'][col].apply(lambda x: ','.join(x.keys()))


	return results, config


def processFile(filename, config):

	progress(filename,0)
	job = filename.split('.csv')[0]

	#with open(root+'/'+directory+'/'+filename, 'rb') as f:
	#    result = chardet.detect(f.read())  # or readline if the file is large
	#    #print result['encoding']
	progress(filename,.05)

	judgments = pd.read_csv(filename)#, encoding=result['encoding'])

	#if directory == '':
	#	directory = '/'

#	collection = directory
	collection = ''

	platform = getPlatform(judgments)

	# we must establish which fields were part of the input data and which are output judgments
	# if there is a config, check if there is a definition of which fields to use
	#config = []
	# else use the default and select them automatically
	config = getColumnTypes(judgments, config)

	# remove rows where the worker did not give an answer (AMT issue)
	empty_rows = set()
	for col in config.outputColumns:
		empty_rows = empty_rows.union(judgments[pd.isnull(judgments[col]) == True].index)
	for col in config.outputColumns:
		judgments = judgments[pd.isnull(judgments[col]) == False]
	judgments = judgments.reset_index(drop=True)
	if len(empty_rows) > 0:
		if len(empty_rows) == 1:
			logging.warning(str(len(empty_rows)) + " row with incomplete information in output columns was removed.")
		else:
			logging.warning(str(len(empty_rows)) + " rows with incomplete information in output columns were removed.")

	# allow customization of the judgments
	judgments = config.processJudgments(judgments)

	# update the config after the preprocessing of judgments
	config = getColumnTypes(judgments, config)
	progress(filename,.1)

	allColumns = dict(config.input.items() + config.output.items() + platform.items())
	judgments = judgments.rename(columns=allColumns)

	# remove columns we don't care about
	judgments = judgments[allColumns.values()]

	judgments['job'] = job
	progress(filename,.15)

	# make output values safe keys
	for col in config.output.values():
		if type(judgments[col].iloc[0]) is dict:
			logging.info("Values stored as dictionary")
			if config.open_ended_task:
				judgments[col] = judgments[col].apply(lambda x: OrderedCounter(x))
			else:
				judgements[col] = judgements[col].apply(lambda x: createOrderedCounter(OrderedCounter(x), config.annotation_vector))	
		else:
			logging.info("Values not stored as dictionary")
			if config.open_ended_task:
				judgments[col] = judgments[col].apply(lambda x: OrderedCounter(x.split(config.annotation_separator)))
			else:
				judgments[col] = judgments[col].apply(lambda x: createOrderedCounter(OrderedCounter(x.split(config.annotation_separator)), config.annotation_vector))

	judgments['started'] = judgments['started'].apply(lambda x: pd.to_datetime(str(x)))
	judgments['submitted'] = judgments['submitted'].apply(lambda x: pd.to_datetime(str(x)))
	judgments['duration'] = judgments.apply(lambda row: (row['submitted'] - row['started']).seconds, axis=1)

	# remove units with just 1 judgment
	units_1work = judgments.groupby('unit').filter(lambda x: len(x) == 1)["unit"]
	judgments = judgments[~judgments['unit'].isin(units_1work)]
	judgments = judgments.reset_index(drop=True)
	if len(units_1work) > 0:
		if len(units_1work) == 1:
			logging.warning(str(len(units_1work)) + " Media Unit that was annotated by only 1 Worker was omitted, since agreement cannot be calculated.")
		else:
			logging.warning(str(len(units_1work)) + " Media Units that were annotated by only 1 Worker were omitted, since agreement cannot be calculated.")


	progress(filename,.2)


	# 


	#
	# aggregate units
	#
	units = Unit.aggregate(judgments, config)
	progress(filename,.25)





	#
	# compute worker agreement
	#
	#for col in config.output.values():
	#	judgments[col+'.agreement'] = judgments.apply(lambda row: Worker.getUnitAgreement(row[col], units.at[row['unit'], col]), axis=1)	
	#	judgments[col+'.count'] = judgments[col].apply(lambda x: sum(x.values()))	
		#judgments[col+'.unique'] = judgments[col].apply(lambda x: len(x))	
	progress(filename,.3)

	#judgments['worker-cosine'] = 1 - judgments.apply(lambda row: np.array([row[col+'.agreement'] for col in config.output.values()]).mean(), axis=1)
	progress(filename,.35)






	#
	# aggregate workers
	#
	workers = Worker.aggregate(judgments, config)
	progress(filename,.4)


	# get the thresholds
	#workerAgreementThreshold = workers['worker-agreement'].mean() - (2 * workers['worker-agreement'].std())
	#workerCosineThreshold = judgments['worker-cosine'].mean() + (2 * judgments['worker-cosine'].std())

	#
	# tag spammers
	#
	#workers['spam'] = (workers['worker-agreement'] < workerAgreementThreshold) & (workers['worker-cosine'] > workerCosineThreshold)
	progress(filename,.45)


	# tag judgments that were spam
	#judgments['spam'] = judgments['worker'].apply(lambda x: workers.at[x,'spam'])
	#filteredJudgments = judgments[judgments['spam'] == False]

	#
	# aggregate units
	#
	#units = Unit.aggregate(filteredJudgments, config)
	units = Unit.aggregate(judgments, config)
	progress(filename,.8)



	#
	# aggregate annotations
	# i.e. output columns
	#	
	
	annotations = pd.DataFrame()
	for col in config.output.values():
#		annotations[col] = pd.Series(judgments[col].sum())
		res = pd.DataFrame(judgments[col].apply(lambda x: pd.Series(x.keys()).value_counts()).sum(),columns=[col])
		annotations = pd.concat([annotations, res], axis=0)
	progress(filename,.85)


	
	#
	# aggregate job
	#
	#job = Job.aggregate(units, filteredJudgments, workers, config)
	job = Job.aggregate(units, judgments, workers, config)
	#job['spam'] = workers['spam'].sum() / float(workers['spam'].count())
	#job['spam.judgments'] = workers['spam'].sum()
	#job['spam.workers'] = workers['spam'].count()
	#job['workerAgreementThreshold'] = workerAgreementThreshold
	#job['workerCosineThreshold'] = workerCosineThreshold
	progress(filename,.9)




	# Clean up judgments
	# remove input columns from judgments
	outputCol = [col for col in judgments.columns.values if col.startswith('output') or col.startswith('metric')]
	#judgments = judgments[outputCol + platform.values() + ['duration','job','spam']]
	judgments = judgments[outputCol + platform.values() + ['duration','job']]
	
	# set judgment id as index
	judgments.set_index('judgment', inplace=True)
	progress(filename,.95)

	# measure performance with ground truth
	#job, units = groundtruth.process(job, units.copy(), config.groundtruth)


	progress(filename,1)
	
	# add missing vector values if closed task
	for col in config.output.values():
		try:
			openended = config.open_ended_task
			for idx in list(units.index):
				for relation in config.annotation_vector:
					if relation not in units[col][idx]:
						units[col][idx].update({relation : 0})	
		except AttributeError:
			continue

	return {
		'jobs' : job, 
		'units' : units,
		'workers' : workers,
		'judgments' : judgments,
		'annotations' : annotations,
		}, config

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

	# returns a list of columns that contain are input content
	config.input = {}
	config.output = {}

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
	fields = map(lambda x: pattern.sub(' ', x).strip().replace(' ', '_'), re.split(',|\||\n',cleanField))
	
	fields = [f for f in fields if len(f) > 0]
	
	if len(fields):
		return fields
	else:
		return ['__None__']

