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
        for col in config.output.values():
            # for each vector in the unit get the unit metrics
            units[col+'.metrics'] = units[col].apply(lambda x: Unit.getMetrics(x))

        # aggregate unit metrics
        metrics = units[config.output.values()[0]+'.metrics'].iloc[0].keys()
        for val in metrics:
            units['metrics.avg_'+val] = units.apply(lambda row: np.mean([row[x+'.metrics'][val] for x in config.output.values()]), axis=1)

        # sort columns
        units = units.reindex_axis(sorted(units.columns), axis=1)

        return units

    @staticmethod
    def getMetrics(vector):
        # for each vector in the unit return a set of metrics
        metrics = {}
        #for vector in vectors:

        metrics['magnitude'] = Unit.get_magnitude(vector)
        metrics['norm_magnitude'] = Unit.get_norm_magnitude(vector)
        cosine_vector = Unit.get_cosine_vector(vector)
        metrics['max_relation_Cos'] = max(cosine_vector.values())
        metrics['vector_size'] = len(vector)

#        averages = Unit.getAverages(metrics)
#        metrics.update(averages)

        return metrics

    @staticmethod
    def getAverages(vectors):
        averages = {}
        keys = vectors[vectors.keys()[0]].keys()
        for k in keys:
            averages['avg_'+k] = np.array([vectors[v][k] for v in vectors]).mean()
        return averages

    @staticmethod
    def getWorkerMetrics(judgments, unitVectors):

        metrics = {}
        for j in judgments:
            judgment = judgments[j]
            metrics[judgment.worker] = {}

            agreement = Unit.getWorkerAgreement(judgment.annotations, unitVectors)
            metrics[judgment.worker]['agreement'] = agreement

            #judgment.setAgreement(agreement)

        averages = Unit.getAverages(metrics)
        metrics.update(averages)

        return metrics

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
    def getWorkerAgreement(workerVector, unitVector):
        print workerVector
        print unitVector
        # loop through vectors
        # for each vector get the agreement between the workers
        # then get the average for the worker.
        sum_cos = 0.0
        count = 0
        for wv in workerVector:
            sum_cos += Unit.getVectorAgreement(workerVector[wv], unitVector[wv])
            count += 1

        if count == 0:
            return 0
        
        return sum_cos/(1.0 * count)


