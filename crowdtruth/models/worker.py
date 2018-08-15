import numpy as np
import pandas as pd

class Worker():


    @staticmethod
    def aggregate(judgments, config):

        workers = judgments.copy().groupby('worker')

        agg = {
            'job' : 'nunique',
            'unit' : 'nunique',
            'judgment' : 'nunique',
            'duration' : 'mean'
            }
        for col in config.output.values():
            agg[col+'.count'] = 'mean'

        workers = workers.agg(agg)

        return workers
