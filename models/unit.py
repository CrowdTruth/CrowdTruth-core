import datetime
import numpy as np
import scipy.spatial as spatial


class Unit():


    @staticmethod
    def aggregate(judgments, config):

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

        #
        # get unit metrics
        #

        # for each vector in the unit get the unit metrics
        units = units.apply(lambda row: Unit.getMetrics(row, config), axis=1)

        metrics = ['cos_clarity','unique_annotations','annotations']

        # aggregate unit metrics
        for val in metrics:
            units['metrics.avg_'+val] = units.apply(lambda row: np.mean([row[col+'.'+val] for col in config.output.values()]), axis=1)

        # sort columns
        units = units.reindex_axis(sorted(units.columns), axis=1)

        return units

    @staticmethod
    def getMetrics(row, config):

        for col in config.output.values():

            # for each vector in the unit return a set of metrics
            #metrics = {}
            #for vector in vectors:

            #metrics['magnitude'] = Unit.get_magnitude(vector)
            #metrics['norm_magnitude'] = Unit.get_norm_magnitude(vector)
            cosine_vector = Unit.get_cosine_vector(row[col])
            row[col+'.cos_clarity'] = max(cosine_vector.values())
            row[col+'.unique_annotations'] = len(row[col])
            row[col+'.annotations'] = sum(row[col].values())

    #        averages = Unit.getAverages(metrics)
    #        metrics.update(averages)

        return row

    @staticmethod
    def getWorkerMetrics(judgments, unitVectors):

        metrics = {}
        for j in judgments:
            judgment = judgments[j]
            metrics[judgment.worker] = {}

            cosine = Unit.getWorkerCosine(judgment.annotations, unitVectors)
            metrics[judgment.worker]['worker-cosine'] = cosine

            #judgment.setAgreement(agreement)

        averages = Unit.getAggregateMetrics(metrics, judgments)
        metrics.update(averages)

        return metrics

    @staticmethod
    def getAggregateMetrics(vectors):
        averages = {}
        keys = vectors[vectors.keys()[0]].keys()
        for k in keys:
            averages['avg_'+k] = np.array([vectors[v][k] for v in vectors]).mean()
        return averages


    @staticmethod
    def get_magnitude(vector):
        return np.linalg.norm(vector.values())

    @staticmethod
    def get_norm_magnitude(vector):
        ann_values = vector.values()
        sum_ann_values = sum(ann_values)
        if sum_ann_values == 0:
            return 0
        return np.linalg.norm(ann_values) / sum_ann_values

    @staticmethod
    def get_cosine_vector(vector):
        cosine_vector = {}

        # don't change ann_values vector before extracting both
        # the keys and the values for preserving the order
        ann_keys = vector.keys()
        ann_values = vector.values()
        ann_length = len(ann_keys)

        #if the ann is the zero vector cosine returns error
        if sum(ann_values) == 0:
            return Unit.ann_dict

        for iter in range(0, ann_length):
            #create the ann_keys[iter] relation vector
            unit_vec = np.zeros(ann_length)
            unit_vec[iter] = 1.0
            #compute the cosine measure
            if (np.count_nonzero(ann_values) == 0):
                rel_cosine = 0
            else:
                rel_cosine = 1 - spatial.distance.cosine(unit_vec, ann_values)

            cosine_vector[ann_keys[iter]] = rel_cosine

        return cosine_vector

    @staticmethod
    def getWorkerCosine(workerVector, unitVector):
        #print workerVector
        #print unitVector


        
        # loop through vectors
        # for each vector get the agreement between the workers
        # then get the average for the worker.
        sum_cos = 0.0
        count = 0
        for wv in workerVector:
            sum_cos += Unit.getVectorCosine(workerVector[wv], unitVector[wv])
            count += 1

        if count == 0:
            return 0
        
        return sum_cos/(1.0 * count)


