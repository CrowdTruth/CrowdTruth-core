class DefaultConfig():

	name = '' # collection name
	inputColumns = [] # inputColumns to use
	outputColumns = [] # outputColumns to use
	customPlatformColumns = []
	open_ended_task = True
	annotation_vector = []

	units = [] 	# units to use
	workers = [] # workers to use
	jobs = [] # jobs to use

	csv_file_separator = ','
	annotation_separator = ','

	def processUnit(self, unit):
		return True

	def processWorker(self, worker):
		return True

	def processJudgments(self, judgments):
		return judgments

	def processResults(self, results, config=[]):
		return results