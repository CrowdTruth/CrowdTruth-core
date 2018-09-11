"""
Initialization of CrowdTruth metrics
"""
import logging
import math

from collections import Counter

import numpy as np
import pandas as pd

SMALL_NUMBER_CONST = 0.00000001

class Metrics():
    """
    Computes and applies the CrowdTruth metrics for evaluating units, workers and annotations.
    """

    # Unit Quality Score
    @staticmethod
    def unit_quality_score(unit_id, unit_work_ann_dict, wqs, aqs):
        """
        Computes the unit quality score.

        The unit quality score (UQS) is computed as the average cosine similarity between
        all worker vectors for a given unit, weighted by the worker quality (WQS) and the
        annotation quality (AQS). The goal is to capture the degree of agreement in annotating
        the media unit.

        Through the weighted average, workers and annotations with lower quality will have
        less of an impact on the final score.

        To weigh the metrics with the annotation quality, we compute weighted_cosine, the weighted
        version of the cosine similarity.

        Args:
            unit_id: Unit id.
            unit_work_ann_dict: A dictionary that contains all the workers judgments for the unit.
            aqs: Dict of annotation_id (string) that contains the annotation quality score (float)
            wqs: Dict of worker_id (string) that contains the worker quality score (float)

        Returns:
            The quality score (UQS) of the given unit.
        """

        uqs_numerator = 0.0
        uqs_denominator = 0.0
        worker_ids = list(unit_work_ann_dict[unit_id].keys())

        for worker_i in range(len(worker_ids) - 1):
            for worker_j in range(worker_i + 1, len(worker_ids)):
                numerator = 0.0
                denominator_i = 0.0
                denominator_j = 0.0

                worker_i_vector = unit_work_ann_dict[unit_id][worker_ids[worker_i]]
                worker_j_vector = unit_work_ann_dict[unit_id][worker_ids[worker_j]]

                for ann in worker_i_vector:
                    worker_i_vector_ann = worker_i_vector[ann]
                    worker_j_vector_ann = worker_j_vector[ann]
                    numerator += aqs[ann] * (worker_i_vector_ann * worker_j_vector_ann)
                    denominator_i += aqs[ann] * (worker_i_vector_ann * worker_i_vector_ann)
                    denominator_j += aqs[ann] * (worker_j_vector_ann * worker_j_vector_ann)

                weighted_cosine = numerator / math.sqrt(denominator_i * denominator_j)

                uqs_numerator += weighted_cosine * wqs[worker_ids[worker_i]] * \
                                 wqs[worker_ids[worker_j]]
                uqs_denominator += wqs[worker_ids[worker_i]] * wqs[worker_ids[worker_j]]

        if uqs_denominator < SMALL_NUMBER_CONST:
            uqs_denominator = SMALL_NUMBER_CONST
        return uqs_numerator / uqs_denominator


    # Worker - Unit Agreement
    @staticmethod
    def worker_unit_agreement(worker_id, unit_ann_dict, work_unit_ann_dict, uqs, aqs, wqs):
        """
        Computes the worker agreement on a unit.

        The worker unit agreement (WUA) is the average cosine distance between the annotations
        of a worker i and all the other annotations for the units they have worked on,
        weighted by the unit and annotation quality. It calculates how much a worker disagrees
        with the crowd on a unit basis.

        Through the weighted average, units and anntation with lower quality will have less
        of an impact on the final score.

        Args:
            worker_id: Worker id.
            unit_ann_dict: Dictionary of units and their aggregated annotations.
            work_unit_ann_dict: Dictionary of units (and its annotation) annotated by the worker.
            uqs: Dict unit_id that contains the unit quality scores (float).
            aqs: Dict of annotation_id (string) that contains the annotation quality scores (float).
            wqs: Dict of worker_id (string) that contains the worker quality scores (float).

        Returns:
            The worker unit agreement score for the given worker.
        """

        wsa_numerator = 0.0
        wsa_denominator = 0.0
        work_unit_ann_dict_worker_id = work_unit_ann_dict[worker_id]

        for unit_id in work_unit_ann_dict_worker_id:
            numerator = 0.0
            denominator_w = 0.0
            denominator_s = 0.0

            worker_vector = work_unit_ann_dict[worker_id][unit_id]
            unit_vector = unit_ann_dict[unit_id]

            for ann in worker_vector:
                worker_vector_ann = worker_vector[ann] * wqs
                unit_vector_ann = unit_vector[ann]

                numerator += aqs[ann] * worker_vector_ann * \
                    (unit_vector_ann - worker_vector_ann)
                denominator_w += aqs[ann] * \
                    (worker_vector_ann * worker_vector_ann)
                denominator_s += aqs[ann] * ( \
                    (unit_vector_ann - worker_vector_ann) * \
                    (unit_vector_ann - worker_vector_ann))
            weighted_cosine = None
            if math.sqrt(denominator_w * denominator_s) < SMALL_NUMBER_CONST:
                weighted_cosine = SMALL_NUMBER_CONST
            else:
                weighted_cosine = numerator / math.sqrt(denominator_w * denominator_s)
            wsa_numerator += weighted_cosine * uqs[unit_id]
            wsa_denominator += uqs[unit_id]
        if wsa_denominator < SMALL_NUMBER_CONST:
            wsa_denominator = SMALL_NUMBER_CONST
        return wsa_numerator / wsa_denominator

    # Worker - Worker Agreement
    @staticmethod
    def worker_worker_agreement(worker_id, work_unit_ann_dict, unit_work_ann_dict, wqs, uqs, aqs):
        """
        Computes the agreement between every two workers.

        The worker-worker agreement (WWA) is the average cosine distance between the annotations of
        a worker i and all other workers that have worked on the same media units as worker i,
        weighted by the worker and annotation qualities.

        The metric gives an indication as to whether there are consisently like-minded workers.
        This is useful for identifying communities of thought.

        Through the weighted average, workers and annotations with lower quality will have less
        of an impact on the final score of the given worker.

        Args:
            worker_id: Worker id.
            work_unit_ann_dict: Dictionary of worker annotation vectors on annotated units.
            unit_work_ann_dict: Dictionary of unit annotation vectors.
            uqs: Dict unit_id that contains the unit quality scores (float).
            aqs: Dict of annotation_id (string) that contains the annotation quality scores (float).
            wqs: Dict of worker_id (string) that contains the worker quality scores (float).

        Returns:
            The worker worker agreement score for the given worker.
        """

        wwa_numerator = 0.0
        wwa_denominator = 0.0

        worker_vector = work_unit_ann_dict[worker_id]
        unit_ids = list(work_unit_ann_dict[worker_id].keys())

        for unit_id in unit_ids:
            wv_unit_id = worker_vector[unit_id]
            unit_work_ann_dict_unit_id = unit_work_ann_dict[unit_id]
            for other_workid in unit_work_ann_dict_unit_id:
                if worker_id != other_workid:
                    numerator = 0.0
                    denominator_w = 0.0
                    denominator_ow = 0.0

                    unit_work_ann_dict_uid_oworkid = unit_work_ann_dict_unit_id[other_workid]
                    for ann in wv_unit_id:
                        unit_work_ann_dict_uid_oworkid_ann = unit_work_ann_dict_uid_oworkid[ann]
                        wv_unit_id_ann = wv_unit_id[ann]

                        numerator += aqs[ann] * (wv_unit_id_ann * \
                                     unit_work_ann_dict_uid_oworkid_ann)

                        denominator_w += aqs[ann] * (wv_unit_id_ann * wv_unit_id_ann)

                        denominator_ow += aqs[ann] * \
                                         (unit_work_ann_dict_uid_oworkid_ann *\
                                          unit_work_ann_dict_uid_oworkid_ann)

                    weighted_cosine = numerator / math.sqrt(denominator_w * denominator_ow)
                    # pdb.set_trace()
                    wwa_numerator += weighted_cosine * wqs[other_workid] * uqs[unit_id]
                    wwa_denominator += wqs[other_workid] * uqs[unit_id]
        if wwa_denominator < SMALL_NUMBER_CONST:
            wwa_denominator = SMALL_NUMBER_CONST
        return wwa_numerator / wwa_denominator



    # Unit - Annotation Score (UAS)
    @staticmethod
    def unit_annotation_score(unit_id, annotation, unit_work_annotation_dict, wqs):
        """
        Computes the unit annotation score.

        The unit - annotation score (UAS) calculates the likelihood that annotation a
        is expressed in unit u. It is the ratio of the number of workers that picked
        annotation a over all workers that annotated the unit, weighted by the worker quality.

        Args:
            unit_id: Unit id.
            annotation: Annotation.
            unit_work_annotation_dict: Dictionary of unit annotation vectors.
            wqs: Dict of worker_id (string) that contains the worker quality scores (float).

        Returns:
            The unit annotation score for the given unit and annotation.
        """

        uas_numerator = 0.0
        uas_denominator = 0.0

        worker_ids = unit_work_annotation_dict[unit_id]
        for worker_id in worker_ids:
            uas_numerator += worker_ids[worker_id][annotation] * wqs[worker_id]
            uas_denominator += wqs[worker_id]
        if uas_denominator < SMALL_NUMBER_CONST:
            uas_denominator = SMALL_NUMBER_CONST
        return uas_numerator / uas_denominator

    @staticmethod
    def compute_ann_quality_factors(numerator, denominator, work_unit_ann_dict_worker_i, \
                                    work_unit_ann_dict_worker_j, ann, uqs):
        """
        Computes the factors for each unit annotation.

        Args:
            numerator: Current numerator
            denominator: Current denominator
            work_unit_ann_dict_worker_i: Dict of worker i annotation vectors on annotated units.
            work_unit_ann_dict_worker_j: Dict of worker j annotation vectors on annotated units.
            ann: Annotation value
            uqs: Dict unit_id that contains the unit quality scores (float).

        Returns:
            The annotation quality factors.
        """
        for unit_id, work_unit_ann_dict_work_i_unit in work_unit_ann_dict_worker_i.items():
            if unit_id in work_unit_ann_dict_worker_j:
                work_unit_ann_dict_work_j_unit = work_unit_ann_dict_worker_j[unit_id]

                work_unit_ann_dict_wj_unit_ann = work_unit_ann_dict_work_j_unit[ann]

                def compute_numerator_aqs(unit_id_ann_value, worker_i_ann_value, \
                                                          worker_j_ann_value):
                    """ compute numerator """
                    numerator = unit_id_ann_value * worker_i_ann_value * \
                                                worker_j_ann_value
                    return numerator

                def compute_denominator_aqs(unit_id_ann_value, worker_j_ann_value):
                    """ compute denominator """
                    denominator = unit_id_ann_value * worker_j_ann_value
                    return denominator

                numerator += compute_numerator_aqs(uqs[unit_id], \
                                                    work_unit_ann_dict_work_i_unit[ann], \
                                                    work_unit_ann_dict_wj_unit_ann)
                denominator += compute_denominator_aqs(uqs[unit_id], \
                                                        work_unit_ann_dict_wj_unit_ann)
        return numerator, denominator

    @staticmethod
    def aqs_dict(annotations, aqs_numerator, aqs_denominator):
        """
        Create the dictionary of annotation quality score values.

        Args:
            annotations: Dictionary of annotations.
            aqs_numerator: Annotation numerator.
            aqs_denominator: Annotation denominator.


        Returns:
            The dictionary of annotation quality scores.
        """

        aqs = dict()
        for ann in annotations:
            if aqs_denominator[ann] > SMALL_NUMBER_CONST:
                aqs[ann] = aqs_numerator[ann] / aqs_denominator[ann]
                # prevent division by zero by storing very small value instead
                if aqs[ann] < SMALL_NUMBER_CONST:
                    aqs[ann] = SMALL_NUMBER_CONST
            else:
                aqs[ann] = SMALL_NUMBER_CONST
        return aqs


    # Annotation Quality Score (AQS)
    @staticmethod
    def annotation_quality_score(annotations, work_unit_ann_dict, uqs, wqs):
        """
        Computes the annotation quality score.

        The annotation quality score AQS calculates the agreement of selecting an annotation a,
        over all the units it appears in. Therefore, it is only applicable to closed tasks, where
        the same annotation set is used for all units. It is based on the probability that if a
        worker j annotates annotation a in a unit, worker i will also annotate it.

        The annotation quality score is the weighted average of these probabilities for all possible
        pairs of workers. Through the weighted average, units and workers with lower quality will
        have less of an impact on the final score of the annotation.

        Args:
            annotations: Possible annotations.
            work_unit_annotation_dict: Dictionary of worker annotation vectors on annotated units.
            uqs: Dict unit_id that contains the unit quality scores (float).
            wqs: Dict of worker_id (string) that contains the worker quality scores (float).

        Returns:
            The worker worker agreement score for the given worker.
        """

        aqs_numerator = dict()
        aqs_denominator = dict()

        for ann in annotations:
            aqs_numerator[ann] = 0.0
            aqs_denominator[ann] = 0.0

        for worker_i, work_unit_ann_dict_worker_i in work_unit_ann_dict.items():
            #work_unit_ann_dict_worker_i = work_unit_ann_dict[worker_i]
            work_unit_ann_dict_i_keys = list(work_unit_ann_dict_worker_i.keys())
            for worker_j, work_unit_ann_dict_worker_j in work_unit_ann_dict.items():
                #work_unit_ann_dict_worker_j = work_unit_ann_dict[worker_j]
                work_unit_ann_dict_j_keys = list(work_unit_ann_dict_worker_j.keys())

                length_keys = len(np.intersect1d(np.array(work_unit_ann_dict_i_keys), \
                                                 np.array(work_unit_ann_dict_j_keys)))

                if worker_i != worker_j and length_keys > 0:
                    for ann in annotations:
                        numerator = 0.0
                        denominator = 0.0

                        numerator, denominator = Metrics.compute_ann_quality_factors(numerator, \
                                                    denominator, work_unit_ann_dict_worker_i, \
                                                    work_unit_ann_dict_worker_j, ann, uqs)

                        if denominator > 0:
                            aqs_numerator[ann] += wqs[worker_i] * wqs[worker_j] * \
                                                        numerator / denominator
                            aqs_denominator[ann] += wqs[worker_i] * wqs[worker_j]

        return Metrics.aqs_dict(annotations, aqs_numerator, aqs_denominator)


    @staticmethod
    def run(results, config, max_delta=0.001):
        '''
        iteratively run the CrowdTruth metrics
        '''

        judgments = results['judgments'].copy()
        units = results['units'].copy()

        # unit_work_ann_dict, work_unit_ann_dict, unit_ann_dict
        # to be done: change to use all vectors in one unit
        col = list(config.output.values())[0]
        unit_ann_dict = dict(units.copy()[col])

        def expanded_vector(worker, unit):
            '''
            expand the vector of a worker on a given unit
            '''
            vector = Counter()
            for ann in unit:
                if ann in worker:
                    vector[ann] = worker[ann]
                else:
                    vector[ann] = 0
            return vector

        # fill judgment vectors with unit keys
        for index, row in judgments.iterrows():
            judgments.at[index, col] = expanded_vector(row[col], units.at[row['unit'], col])

        unit_work_ann_dict = judgments[['unit', 'worker', col]].copy().groupby('unit')
        unit_work_ann_dict = {name : group.set_index('worker')[col].to_dict() \
                                for name, group in unit_work_ann_dict}

        work_unit_ann_dict = judgments[['worker', 'unit', col]].copy().groupby('worker')
        work_unit_ann_dict = {name : group.set_index('unit')[col].to_dict() \
                                for name, group in work_unit_ann_dict}

        #initialize data structures
        uqs_list = list()
        wqs_list = list()
        wwa_list = list()
        wsa_list = list()
        aqs_list = list()

        uqs = dict((unit_id, 1.0) for unit_id in unit_work_ann_dict)
        wqs = dict((worker_id, 1.0) for worker_id in work_unit_ann_dict)
        wwa = dict((worker_id, 1.0) for worker_id in work_unit_ann_dict)
        wsa = dict((worker_id, 1.0) for worker_id in work_unit_ann_dict)

        uqs_list.append(uqs.copy())
        wqs_list.append(wqs.copy())
        wwa_list.append(wwa.copy())
        wsa_list.append(wsa.copy())

        def init_aqs(config, unit_ann_dict):
            """ initialize aqs depending on whether or not it is an open ended task """
            aqs = dict()
            if not config.open_ended_task:
                aqs_keys = list(unit_ann_dict[list(unit_ann_dict.keys())[0]].keys())
                for ann in aqs_keys:
                    aqs[ann] = 1.0
            else:
                for unit_id in unit_ann_dict:
                    for ann in unit_ann_dict[unit_id]:
                        aqs[ann] = 1.0
            return aqs

        aqs = init_aqs(config, unit_ann_dict)
        aqs_list.append(aqs.copy())

        uqs_len = len(list(uqs.keys())) * 1.0
        wqs_len = len(list(wqs.keys())) * 1.0
        aqs_len = len(list(aqs.keys())) * 1.0

        # compute metrics until stable values
        iterations = 0
        while max_delta >= 0.001:
            uqs_new = dict()
            wqs_new = dict()
            wwa_new = dict()
            wsa_new = dict()

            avg_uqs_delta = 0.0
            avg_wqs_delta = 0.0
            avg_aqs_delta = 0.0
            max_delta = 0.0

            # pdb.set_trace()

            def compute_wqs(wwa_new, wsa_new, wqs_new, work_unit_ann_dict, unit_ann_dict, \
                            unit_work_ann_dict, wqs_list, uqs_list, aqs_list, wqs_len, \
                            max_delta, avg_wqs_delta):
                """ compute worker quality score (WQS) """
                for worker_id, _ in work_unit_ann_dict.items():
                    wwa_new[worker_id] = Metrics.worker_worker_agreement( \
                             worker_id, work_unit_ann_dict, \
                             unit_work_ann_dict, \
                             wqs_list[len(wqs_list) - 1], \
                             uqs_list[len(uqs_list) - 1], \
                             aqs_list[len(aqs_list) - 1])
                    wsa_new[worker_id] = Metrics.worker_unit_agreement( \
                             worker_id, \
                             unit_ann_dict, \
                             work_unit_ann_dict, \
                             uqs_list[len(uqs_list) - 1], \
                             aqs_list[len(aqs_list) - 1], \
                             wqs_list[len(wqs_list) - 1][worker_id])
                    wqs_new[worker_id] = wwa_new[worker_id] * wsa_new[worker_id]
                    max_delta = max(max_delta, \
                                abs(wqs_new[worker_id] - wqs_list[len(wqs_list) - 1][worker_id]))
                    avg_wqs_delta += abs(wqs_new[worker_id] - \
                                         wqs_list[len(wqs_list) - 1][worker_id])
                avg_wqs_delta /= wqs_len

                return wwa_new, wsa_new, wqs_new, max_delta, avg_wqs_delta

            def compute_aqs(aqs, work_unit_ann_dict, uqs_list, wqs_list, aqs_list, aqs_len, max_delta, avg_aqs_delta):
                """ compute annotation quality score (aqs) """
                aqs_new = Metrics.annotation_quality_score(list(aqs.keys()), work_unit_ann_dict, \
                                                        uqs_list[len(uqs_list) - 1], \
                                                        wqs_list[len(wqs_list) - 1])
                for ann, _ in aqs_new.items():
                    max_delta = max(max_delta, abs(aqs_new[ann] - aqs_list[len(aqs_list) - 1][ann]))
                    avg_aqs_delta += abs(aqs_new[ann] - aqs_list[len(aqs_list) - 1][ann])
                avg_aqs_delta /= aqs_len
                return aqs_new, max_delta, avg_aqs_delta

            def compute_uqs(uqs_new, unit_work_ann_dict, wqs_list, aqs_list, uqs_list, uqs_len, max_delta, avg_uqs_delta):
                """ compute unit quality score (uqs) """
                for unit_id, _ in unit_work_ann_dict.items():
                    uqs_new[unit_id] = Metrics.unit_quality_score(unit_id, unit_work_ann_dict, \
                                                                      wqs_list[len(wqs_list) - 1], \
                                                                      aqs_list[len(aqs_list) - 1])
                    max_delta = max(max_delta, \
                                abs(uqs_new[unit_id] - uqs_list[len(uqs_list) - 1][unit_id]))
                    avg_uqs_delta += abs(uqs_new[unit_id] - uqs_list[len(uqs_list) - 1][unit_id])
                avg_uqs_delta /= uqs_len
                return uqs_new, max_delta, avg_uqs_delta

            def reconstruct_unit_ann_dict(unit_ann_dict, work_unit_ann_dict, wqs_new):
                """ reconstruct unit_ann_dict with worker scores """
                new_unit_ann_dict = dict()
                for unit_id, ann_dict in unit_ann_dict.items():
                    new_unit_ann_dict[unit_id] = dict()
                    for ann, _ in ann_dict.items():
                        new_unit_ann_dict[unit_id][ann] = 0.0
                for work_id, srd in work_unit_ann_dict.items():
                    wqs_work_id = wqs_new[work_id]
                    for unit_id, ann_dict in srd.items():
                        for ann, score in ann_dict.items():
                            new_unit_ann_dict[unit_id][ann] += score * wqs_work_id

                return new_unit_ann_dict

            if not config.open_ended_task:
                # compute annotation quality score (aqs)
                aqs_new, max_delta, avg_aqs_delta = compute_aqs(aqs, work_unit_ann_dict, \
                                uqs_list, wqs_list, aqs_list, aqs_len, max_delta, avg_aqs_delta)

            # compute unit quality score (uqs)
            uqs_new, max_delta, avg_uqs_delta = compute_uqs(uqs_new, unit_work_ann_dict, \
                                    wqs_list, aqs_list, uqs_list, uqs_len, max_delta, avg_uqs_delta)

            # compute worker quality score (WQS)
            wwa_new, wsa_new, wqs_new, max_delta, avg_wqs_delta = compute_wqs(\
                        wwa_new, wsa_new, wqs_new, \
                        work_unit_ann_dict, unit_ann_dict, unit_work_ann_dict, wqs_list, \
                        uqs_list, aqs_list, wqs_len, max_delta, avg_wqs_delta)

            # save results for current iteration
            uqs_list.append(uqs_new.copy())
            wqs_list.append(wqs_new.copy())
            wwa_list.append(wwa_new.copy())
            wsa_list.append(wsa_new.copy())
            if not config.open_ended_task:
                aqs_list.append(aqs_new.copy())
            iterations += 1

            unit_ann_dict = reconstruct_unit_ann_dict(unit_ann_dict, work_unit_ann_dict, wqs_new)

            logging.info(str(iterations) + " iterations; max d= " + str(max_delta) + \
                        " ; wqs d= " + str(avg_wqs_delta) + "; uqs d= " + str(avg_uqs_delta) + \
                        "; aqs d= " + str(avg_aqs_delta))

        def save_unit_ann_score(unit_ann_dict, unit_work_ann_dict, iteration_value):
            """ save the unit annotation score for print """
            uas = Counter()
            for unit_id in unit_ann_dict:
                uas[unit_id] = Counter()
                for ann in unit_ann_dict[unit_id]:
                    uas[unit_id][ann] = Metrics.unit_annotation_score(unit_id, \
                                                ann, unit_work_ann_dict, \
                                                iteration_value)
            return uas

        uas = save_unit_ann_score(unit_ann_dict, unit_work_ann_dict, wqs_list[len(wqs_list) - 1])
        uas_initial = save_unit_ann_score(unit_ann_dict, unit_work_ann_dict, wqs_list[0])

        results['units']['uqs'] = pd.Series(uqs_list[-1])
        results['units']['unit_annotation_score'] = pd.Series(uas)
        results['workers']['wqs'] = pd.Series(wqs_list[-1])
        results['workers']['wwa'] = pd.Series(wwa_list[-1])
        results['workers']['wsa'] = pd.Series(wsa_list[-1])
        if not config.open_ended_task:
            results['annotations']['aqs'] = pd.Series(aqs_list[-1])

        results['units']['uqs_initial'] = pd.Series(uqs_list[1])
        results['units']['unit_annotation_score_initial'] = pd.Series(uas_initial)
        results['workers']['wqs_initial'] = pd.Series(wqs_list[1])
        results['workers']['wwa_initial'] = pd.Series(wwa_list[1])
        results['workers']['wsa_initial'] = pd.Series(wsa_list[1])
        if not config.open_ended_task:
            results['annotations']['aqs_initial'] = pd.Series(aqs_list[1])
        return results
