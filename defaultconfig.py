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
	'	customize the results
	'''
	def customizeResults(self, results):
		return results