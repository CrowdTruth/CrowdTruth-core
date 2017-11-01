'''
'	CrowdTruth Configuration File
'	Version 0.1
'''

class Configuration():

	# collection name
	name = ''

	# inputColumns to use
	inputColumns = []
	# outputColumns to use
	outputColumns = []
	
	open_ended_task = True
	annotation_vector = []
	
	column_separator = ','
	judgment_separator = ','

	# units to use
	units = []
	# workers to use
	workers = []
	# jobs to use
	jobs = []


	def processUnit(self, unit):
		return True

	def processWorker(self, worker):
		return True

	'''
	'	customize the judgments before being processed
	'''
	def processJudgments(self, judgments):
		return judgments

	'''
	'	customize the results
	'''
	def processResults(self, results, config=[]):
		return results
