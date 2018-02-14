import datetime
import re, string
import numpy as np

class Job():

	@staticmethod
	def aggregate(units, judgments, workers, config):

		# each output column dict is summed

		agg = {
			'unit' : 'nunique',
			'judgment' : 'nunique',
			'worker' : 'nunique',
			'duration' : 'mean'
			#'worker-cosine' : 'mean'
		}
		job = judgments.groupby('job').agg(agg)

		#job['worker-agreement'] = workers['worker-agreement'].mean()

		# compute job runtime
		runtime = (max(judgments['submitted']) - min(judgments['started']))
		job['runtime'] = float(runtime.days) * 24 + float(runtime.seconds) / 3600
		job['runtime.per_unit'] = job['runtime'] / job['unit']
		job['judgments.per.worker'] = job['judgment'] / job['worker']


		agg = {}
		#metrics = ['cos_clarity','unique_annotations','annotations']

#		for metric in metrics:
#
#			for col in config.output.values():
#				# aggregate unit metrics
#				job[col+'.'+metric] = units[col+'.'+metric].mean()
#			job['metrics.avg_'+metric] = units['metrics.avg_'+metric].mean()
		

		job = job.reindex_axis(sorted(job.columns), axis=1)
		

		return job

