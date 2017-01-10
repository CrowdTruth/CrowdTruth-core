import datetime
import numpy as np
import scipy.spatial as spatial


class Unit():

    def __init__(self):
        id = fields.CharField(primary_key=True)
        collection = fields.CharField()
        job = fields.CharField()
        workers = fields.ListField()
        judgments = fields.ListField()
        platform = fields.CharField()
        content = fields.DictField()

        now = datetime.datetime.utcnow()
        created = fields.DateTimeField(default=now)
        updated = fields.DateTimeField(default=now)

        workers = fields.ListField()
        metrics = fields.DictField()
        results = fields.DictField()



    @staticmethod
    def getResults(judgments):
        vectors = {}
        
        for index, judgment in judgments.iteritems():
        # for each judgment in this vector
            for vector in judgment['results']:
                # each vector in this judgment
                vectors[vector] = vectors.get(vector, {})
                annotationVector = judgment['results'][vector]

                for key in annotationVector:
                    # each key in this annotationVector
                    vectors[vector][key] = vectors[vector].get(key, 0) + 1
        return vectors

    @staticmethod
    def getMetrics(judgments):
        
        metrics = {}

        metrics['judgments'] = Unit.getJudgmentMetrics(judgments)



        #metrics['workers'] = self.getWorkerMetrics(judgments)
        #metrics['workers']['count'] = len(self.results['raw'])
    '''

        return results

    def get_cosine_vector(self):
        if self.cosine_vector:
            return self.cosine_vector

        self.cosine_vector = VectorMetrics(self.unit_vector).get_cosine_vector()

        return self.cosine_vector

    def get_no_annotators(self):
        return self.no_annotators


    '''



    @staticmethod
    def getUnitMetrics(vector):
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

    @staticmethod
    def getVectorAgreement(workerVector, unitVector):
        unitArray = np.zeros(len(unitVector))
        workerArray = np.zeros(len(unitVector))
        index = 0
        for key in unitVector.keys():
            unitArray[index] = unitVector[key] - workerVector.get(key, 0)
            workerArray[index] = workerVector.get(key, 0)
            index += 1

        if (np.count_nonzero(unitArray) == 0) or (np.count_nonzero(workerArray) == 0):
            return 0

        rel_cosine = spatial.distance.cosine(unitArray, workerArray)
        return 1 - rel_cosine
