import datetime
import unit
import numpy as np
import itertools
import pandas as pd
from collections import Counter
from datetime import datetime
from collections import defaultdict
import scipy.spatial as spatial


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