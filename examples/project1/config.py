'''
'	CrowdTruth Configuration File
'	Version 0.1
'''

class Configuration():

	# collection name
	name = 'Project name'

	# InputColumns to select. If empty these columns are identified automatically.
	inputColumns = []
	# OutputColumns to use. If empty these columns are identified automatically.
	outputColumns = []


	# Units to use
	units = []
	# Workers to use
	workers = []
	# Jobs to use
	jobs = []


	def processUnit(unit):
		return True

	def processWorker(worker):
		return True