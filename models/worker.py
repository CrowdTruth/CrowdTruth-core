import datetime
from models.unit import *
import numpy as np
import itertools
import pandas as pd
from collections import Counter

class Worker():


    @staticmethod
    def aggregate(judgments, config):

        workers = judgments.copy().groupby('worker')

        # get workerWorkerAgreement on all fields
        workerWorkerAgreement = Worker.getAvgWorkerWorkerAgreement(workers, config.output.values())

        agg = {
            'job' : 'nunique',
            'unit' : 'nunique',
            'judgment' : 'nunique',
            'duration' : 'mean',
            'worker-cosine' : 'mean'
            }
        for col in config.output.values():
            agg[col+'.count'] = 'mean'

        workers = workers.agg(agg)

        #workers = pd.concat([workers, workerWorkerAgreement], axis=1)
        workers['worker-agreement'] = workerWorkerAgreement['agreement']

        #workerAgreement = Worker.getAvgWorkerAgreement(workers)
        return workers


    def getFeatures(self):
        self.features = {}
        judgments = Judgment.objects.raw({'worker': self.id})

        self.features['judgments'] = judgments.count()

        self.features['units'] = self.getMetrics(judgments)


    @staticmethod
    def getMetrics(judgments):

        metrics = {}
        for judgment in judgments:
            unit = Unit.objects.get({'_id': judgment.unit})
            #unit = judgment.unit
            worker = judgment.worker
            metrics[unit.id] = {}

            #metrics[unit]['annotations'] = self.getAnnotationsPerUnit(judgment.annotations)
            metrics[unit.id]['worker_agreement'] = unit.features['workers'][worker]['agreement']

            #judgment.features['agreement']
            
            #metrics[unit]['similarity'] = self.get_w_u_similarity(judgment.annotationVector, unit.results.raw)
        #metrics[unit]['worker_cosine'] = self.get_worker_cosine(judgment.annotationVector, unit.results.raw)
        
        averages = self.getAverages(metrics)
        metrics.update(averages)

        return metrics


    def getAverages(self, vectors):
        averages = {}
        keys = vectors[vectors.keys()[0]].keys()
        for k in keys:
            averages['avg_'+k] = np.array([vectors[v][k] for v in vectors]).mean()
        return averages
 
    def getAnnotationsPerUnit(self, vectors):
        # how many annotations has this worker performed per unit?
        return sum([sum(vectors[v].values()) for v in vectors])


    @staticmethod
    def getAvgWorkerWorkerAgreement(workers, columns):

        # make a list of the workers
        workerList = workers.groups
        
        # create an empty matrix with the workers
        result = pd.DataFrame(index=workerList, columns=workerList)
        
        # compute all combinations of workers so that we do not have to compute each agreement twice
        combinations = list(itertools.combinations(workerList,2))

        for workera, workerb in combinations:
            # for each worker combination compute the agreement
            agreement = Worker.getWorkerWorkerAgreement(workers.get_group(workera), workers.get_group(workerb), columns)

            # save the agreement to both workers
            result[workera][workerb] = agreement
            result[workerb][workera] = agreement

        result = pd.DataFrame(result.mean(), columns=['agreement'])

        return result



        weighted_sum = 0.0
        weighted_count = 0.0
        for worker_id in workers.index:

            worker = workers[worker_id]
            if (self.crowd_agent_id in worker.worker_agreement):
                w_w_agreement = worker.worker_agreement[self.crowd_agent_id]
            else:
                w_w_agreement = self.get_w_w_agreement(workers[worker_id])
                self.worker_agreement[worker_id] = w_w_agreement

            no_common_units = len(self.get_common_units(workers[worker_id]))
            weighted_count += no_common_units
            weighted_sum += no_common_units*w_w_agreement

        if weighted_count == 0.0:
            return 0

        return weighted_sum/(weighted_count * 1.0)


    @staticmethod
    def getWorkerWorkerAgreement(workera, workerb, columns):
        # get the units in common
        units = Worker.getCommonUnits(workera, workerb)

        # if there are no common units we return false. i.e. it should not be counted towards the worker.
        if len(units) == 0:
            return np.NaN
#        return len(units)

        pairs = list()
        workera.set_index('unit', inplace=True)
        workerb.set_index('unit', inplace=True)

        for unit in units:

            # pairwise comparison of all the worker vectors
            for col in columns:

                #
                join = len(workera[col][unit] + workerb[col][unit])
                overlap = len(workera[col][unit] & workerb[col][unit])
                pairs.append(overlap / float(join))

                #print 'join:',join
                #print 'overlap:',overlap

        #print pairs
        #print np.mean(pairs)
        avg = np.mean(pairs)
        if avg > 1:
            print pairs
            print 'WARNING: duplicate worker unit detected'

        return avg

    @staticmethod
    def getCommonUnits(workera, workerb):
        return list(set(workera['unit']) & set(workerb['unit']))

        worker_unit_vectors = worker.get_unit_vectors()
        worker_units = worker_unit_vectors.keys()
        self_units = self.get_unit_vectors().keys()
        common_units = list(set(worker_units) & set(self_units))
        return common_units

    @staticmethod
    def getNormalizedVector(unit):
        worker_unit_vec = self.unit_vectors[unit_id]
        norm_worker_unit_vec = {}
        for key in worker_unit_vec:
            norm_worker_unit_vec[key] = worker_unit_vec[key]/(self.unit_freq[unit_id] * 1.0)
        return norm_worker_unit_vec



    @staticmethod
    def getUnitAgreement(workerVector, unitVector):
        # create an empty array for both the worker and unit vector
        unitArray = np.zeros(len(unitVector))
        workerArray = np.zeros(len(unitVector))
        index = 0
        # substract the worker vector from the unit vector
        for key in unitVector.keys():
            unitArray[index] = unitVector[key] - workerVector.get(key, 0)
            workerArray[index] = workerVector.get(key, 0)
            index += 1

        # return zero if there is no overlap between the vectors
        if (np.count_nonzero(unitArray) == 0) or (np.count_nonzero(workerArray) == 0):
            return 0

        # compute the cosine distance between the unit vector and the worker vector
        rel_cosine = spatial.distance.cosine(unitArray, workerArray)

        # return the agreement as 1 - cosine distance
        return 1 - rel_cosine

