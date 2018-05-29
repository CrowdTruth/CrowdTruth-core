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

	judgments = None
	
	if directory != "":
		logging.info("PROCESSING FOLDER: " + directory)
		files = os.listdir(directory)
		logging.info("FILE LIST: { " + ", ".join(files) + " }")
		for f in files:
		    f_data = pd.read_csv(root+"/"+directory + "/" + f, sep = config.csv_file_separator)
		    
		    if judgments is None:
		    	judgments = f_data
		    else:
		      	judgments = judgments.append(f_data, ignore_index=True)
	else:
		logging.info("PROCESSING FILE: " + filename)
	  	judgments = pd.read_csv(filename, sep = config.csv_file_separator)


	collection = directory

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
	
	allColumns = dict(config.input.items() + config.output.items() + platform.items())
	judgments = judgments.rename(columns=allColumns)

	# remove columns we don't care about
	judgments = judgments[allColumns.values()]

	judgments['job'] = job

	n_judgments = len(judgments)
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
	# pdb.set_trace()

	#
	# aggregate units
	#
	units = Unit.aggregate(judgments, config)


	#
	# compute total number of annotations and total number of unique annotations
	#
	for col in config.output.values():
		judgments[col+'.count'] = judgments[col].apply(lambda x: sum(x.values()))	
		judgments[col+'.unique'] = judgments[col].apply(lambda x: len(x))	


	#
	# aggregate workers
	#
	workers = Worker.aggregate(judgments, config)


	#
	# aggregate annotations, the output columns
	#	
	annotations = pd.DataFrame()
	for col in config.output.values():
		res = pd.DataFrame(judgments[col].apply(lambda x: pd.Series(x.keys()).value_counts()).sum(),columns=[col])
		annotations = pd.concat([annotations, res], axis=0)


	# Clean up judgments
	# remove input columns from judgments
	outputCol = [col for col in judgments.columns.values if col.startswith('output') or col.startswith('metric')]
	judgments = judgments[outputCol + platform.values() + ['duration','job']]
	
	# set judgment id as index
	judgments.set_index('judgment', inplace=True)

	# add missing vector values if closed task
	for col in config.output.values():
		if not config.open_ended_task:
		    for idx in list(units.index):
		        for relation in config.annotation_vector:
		            if relation not in units[col][idx]:
		                units[col][idx].update({relation : 0})
	return { 
		'units' : units,
		'workers' : workers,
		'judgments' : judgments,
		'annotations' : annotations
		}

def getPlatform(df):
	# Get the crowdsourcing platform this file originates to

	if df.columns.values[0] == '_unit_id':
		# FigureEight, CrowdFlower
		return {
			'_id' 			: 'judgment',
			'_unit_id' 		: 'unit',
			'_worker_id' 	: 'worker',
			'_started_at'	: 'started',
			'_created_at'	: 'submitted'
		}
	elif df.columns.values[0] == 'HITId':
		# Mturk
		return {
			'AssignmentId' 	: 'judgment',
			'HITId' 		: 'unit',
			'WorkerId' 		: 'worker',
			'AcceptTime'	: 'started',
			'SubmitTime'	: 'submitted'
		}
	else:
		# Users must define the following columns
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
