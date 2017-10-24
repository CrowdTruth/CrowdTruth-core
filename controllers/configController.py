import os
import sys
import groundtruthController as gt


def getConfig(root, directory):

	if os.path.exists(root+directory+'/config.py'):
		print 'Loading',root+directory
		sys.path.insert(0, root+directory)
		from config import Configuration
		config = Configuration()
		print 'Loaded configuration for',config.name
	else:
		from defaultconfig import Configuration
		config = Configuration()

	config.groundtruth = gt.getGroundTruth(root, directory)

	return config