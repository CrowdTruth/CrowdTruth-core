import datetime
import numpy as np
import scipy.spatial as spatial
import pdb


class Unit():


    @staticmethod
    def aggregate(judgments, config):
	#print(judgments)
        agg = {}
        for col in config.input.values():
            # for each input column the first value is taken. all rows have the same value for each unit.
            agg[col] = 'first'
        for col in config.output.values():
            # each output column dict is summed
            agg[col] = 'sum'
            
        agg['job'] = 'first'
        agg['worker'] = 'count'
        agg['duration'] = 'mean'

        units = judgments.groupby('unit').agg(agg)

        # for each vector in the unit get the unit metrics
        units = units.apply(lambda row: Unit.getMetrics(row, config), axis=1)

        #metrics = ['cos_clarity','unique_annotations','annotations']
        metrics = ['unique_annotations', 'annotations']

        # sort columns
        units = units.reindex_axis(sorted(units.columns), axis=1)

        return units

    @staticmethod
    def getMetrics(row, config):

        for col in config.output.values():

            # for each vector in the unit return a set of metrics
            row[col+'.unique_annotations'] = len(row[col])
            row[col+'.annotations'] = sum(row[col].values())

        return row

