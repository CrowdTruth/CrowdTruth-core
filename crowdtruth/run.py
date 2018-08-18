"""
Module used to run the CrowdTruth metrics.
"""

from crowdtruth.models.metrics import Metrics

def run(data, config):
    """Run the CrowdTruth metrics with the given processing configuration"""

    processed_results = Metrics.run(data, config)
    return processed_results
