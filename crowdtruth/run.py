from models.metrics import *

def run(data, config):
	processed_results = Metrics.run(data, config)
	return processed_results