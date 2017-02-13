from models import *
import pandas as pd
import os

def getGroundTruth(root, directory):
	
	if os.path.exists(root+directory+'/groundtruth.csv'):
		print 'Loaded ground truth'
		return pd.read_csv(root+'/'+directory+'/groundtruth.csv')
	else:
		return pd.DataFrame()


def process(job, units, groundtruth):

	# if there is no ground truth, we can quit this process right away
	if not len(groundtruth.index):
		return job, units

	# get the ground truth for these units
	#gt = groundtruth.ix[units.index.values]
	print groundtruth.head()
	print units.head()

	# get the ground truth identifier. i.e. the column in the units that identifies each unit
	identifier = groundtruth.columns.values[0]


	return job, units


