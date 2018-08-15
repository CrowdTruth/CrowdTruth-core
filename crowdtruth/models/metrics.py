import logging
import math

from collections import Counter

import numpy as np
import pandas as pd

SMALL_NUMBER_CONST = 0.00000001

class Metrics():


    # Sentence Quality Score
    @staticmethod
    def sentence_quality_score(sentence_id, sent_work_rel_dict, wqs, rqs):
        '''
        sentence_id
        work_sent_rel_dict
        rqs: dict of relation_id (string) -> relation quality (float)
        wqs: dict of worker_id (string) -> worker quality score
        '''

        sqs_numerator = 0.0
        sqs_denominator = 0.0
        worker_ids = list(sent_work_rel_dict[sentence_id].keys())

        for worker_i in range(len(worker_ids) - 1):
            for worker_j in range(worker_i + 1, len(worker_ids)):
                # print worker_ids[i] + " - " + worker_ids[j] + "\n"
                numerator = 0.0
                denominator_i = 0.0
                denominator_j = 0.0

                worker_i_vector = sent_work_rel_dict[sentence_id][worker_ids[worker_i]]
                worker_j_vector = sent_work_rel_dict[sentence_id][worker_ids[worker_j]]

                for relation in worker_i_vector:
                    worker_i_vector_rel = worker_i_vector[relation]
                    worker_j_vector_rel = worker_j_vector[relation]
                    numerator += rqs[relation] * (worker_i_vector_rel * worker_j_vector_rel)
                    denominator_i += rqs[relation] * (worker_i_vector_rel * worker_i_vector_rel)
                    denominator_j += rqs[relation] * (worker_j_vector_rel * worker_j_vector_rel)

                weighted_cosine = numerator / math.sqrt(denominator_i * denominator_j)

                sqs_numerator += weighted_cosine * wqs[worker_ids[worker_i]] * \
                                 wqs[worker_ids[worker_j]]
                sqs_denominator += wqs[worker_ids[worker_i]] * wqs[worker_ids[worker_j]]

        if sqs_denominator < SMALL_NUMBER_CONST:
            sqs_denominator = SMALL_NUMBER_CONST
        return sqs_numerator / sqs_denominator


    # Worker - Sentence Agreement
    @staticmethod
    def worker_sentence_agreement(worker_id, sent_rel_dict, work_sent_rel_dict, sqs, rqs):
        '''
        worker_id
        sent_rel_dict
        work_sent_rel_dict
        sentence_vectors: data frame of sentence vectors
        sqs (sentence quality score): dict sentence_id -> sentence quality (float)
        rqs: dict of relation_id (string) -> relation quality (float)
        '''
        wsa_numerator = 0.0
        wsa_denominator = 0.0
        work_sent_rel_dict_worker_id = work_sent_rel_dict[worker_id]

        for sentence_id in work_sent_rel_dict_worker_id:
            numerator = 0.0
            denominator_w = 0.0
            denominator_s = 0.0

            worker_vector = work_sent_rel_dict[worker_id][sentence_id]
            sentence_vector = sent_rel_dict[sentence_id]

            for rel in worker_vector:
                worker_vector_relation = worker_vector[rel]
                sentence_vector_relation = sentence_vector[rel]

                numerator += rqs[rel] * worker_vector_relation * \
                            (sentence_vector_relation - worker_vector_relation)
                denominator_w += rqs[rel] * (worker_vector_relation * worker_vector_relation)
                denominator_s += rqs[rel] * ((sentence_vector_relation - worker_vector_relation) * \
                                            (sentence_vector_relation - worker_vector_relation))
            weighted_cosine = numerator / math.sqrt(denominator_w * denominator_s)
            wsa_numerator += weighted_cosine * sqs[sentence_id]
            wsa_denominator += sqs[sentence_id]
        if wsa_denominator < SMALL_NUMBER_CONST:
            wsa_denominator = SMALL_NUMBER_CONST
        #    # pdb.set_trace()
        return wsa_numerator / wsa_denominator


    # Worker - Worker Agreement
    @staticmethod
    def worker_worker_agreement(worker_id, work_sent_rel_dict, sent_work_rel_dict, wqs, sqs, rqs):
        '''
        worker_id
        work_sent_rel_dict
        sent_work_rel_dict
        worker_vectors: data frame of worker vectors
        sqs (sentence quality score): dict sentence_id -> sentence quality (float)
        rqs: dict of relation_id (string) -> relation quality (float)
        '''

        wwa_numerator = 0.0
        wwa_denominator = 0.0

        worker_vector = work_sent_rel_dict[worker_id]
        sentence_ids = list(work_sent_rel_dict[worker_id].keys())

        for sentence_id in sentence_ids:
            wv_sentence_id = worker_vector[sentence_id]
            sent_work_rel_dict_sentence_id = sent_work_rel_dict[sentence_id]
            for other_worker_id in sent_work_rel_dict_sentence_id:
                if worker_id != other_worker_id:
                    numerator = 0.0
                    denominator_w = 0.0
                    denominator_ow = 0.0

                    sent_work_rel_dict_sentence_id_other_worker_id = sent_work_rel_dict_sentence_id[other_worker_id]
                    for relation in wv_sentence_id:
                        sent_work_rel_dict_sentence_id_other_worker_id_relation = sent_work_rel_dict_sentence_id_other_worker_id[relation]
                        wv_sentence_id_relation = wv_sentence_id[relation]

                        numerator += rqs[relation] * (wv_sentence_id_relation * sent_work_rel_dict_sentence_id_other_worker_id_relation)

                        denominator_w += rqs[relation] * (wv_sentence_id_relation * wv_sentence_id_relation)

                        denominator_ow += rqs[relation] * (sent_work_rel_dict_sentence_id_other_worker_id_relation *
                                                           sent_work_rel_dict_sentence_id_other_worker_id_relation)

                    weighted_cosine = numerator / math.sqrt(denominator_w * denominator_ow)
                    # pdb.set_trace()
                    wwa_numerator += weighted_cosine * wqs[other_worker_id] * sqs[sentence_id]
                    wwa_denominator += wqs[other_worker_id] * sqs[sentence_id]
        if wwa_denominator < SMALL_NUMBER_CONST:
            wwa_denominator = SMALL_NUMBER_CONST
        return wwa_numerator / wwa_denominator



    # Sentence - Relation Score
    @staticmethod
    def sentence_relation_score(sentence_id, relation, sent_work_rel_dict, wqs):
        '''
        sentence_id
        relation
        sent_work_rel_dict
        wqs: dict of workers_id (string) -> worker quality (float)
        '''
        srs_numerator = 0.0
        srs_denominator = 0.0

        worker_ids = sent_work_rel_dict[sentence_id]
        for worker_id in worker_ids:
            srs_numerator += worker_ids[worker_id][relation] * wqs[worker_id]
            srs_denominator += wqs[worker_id]
        if srs_denominator < SMALL_NUMBER_CONST:
            srs_denominator = SMALL_NUMBER_CONST
        return srs_numerator / srs_denominator


    # Relation Quality Score
    @staticmethod
    def relation_quality_score(relations, work_sent_rel_dict, sqs, wqs):
        '''
        relations
        work_sent_rel_dict
        sqs (sentence quality score): dict sentence_id -> sentence quality (float)
        wqs: dict of workers_id (string) -> worker quality (float)
        '''
        rqs_numerator = dict()
        rqs_denominator = dict()

        for relation in relations:
            rqs_numerator[relation] = 0.0
            rqs_denominator[relation] = 0.0

        for worker_i, work_sent_rel_dict_worker_i in work_sent_rel_dict.items():
            #work_sent_rel_dict_worker_i = work_sent_rel_dict[worker_i]
            work_sent_rel_dict_i_keys = list(work_sent_rel_dict_worker_i.keys())
            for worker_j, work_sent_rel_dict_worker_j in work_sent_rel_dict.items():
                #work_sent_rel_dict_worker_j = work_sent_rel_dict[worker_j]
                work_sent_rel_dict_j_keys = list(work_sent_rel_dict_worker_j.keys())

                if worker_i != worker_j and len(np.intersect1d(np.array(work_sent_rel_dict_i_keys), np.array(work_sent_rel_dict_j_keys))) > 0:
                    for relation in relations:
                        numerator = 0.0
                        denominator = 0.0

                        for sentence_id, work_sent_rel_dict_worker_i_sent in work_sent_rel_dict_worker_i.items():
                            if sentence_id in work_sent_rel_dict_worker_j:
                                #work_sent_rel_dict_worker_i_sent = work_sent_rel_dict_worker_i[sentence_id]
                                work_sent_rel_dict_worker_j_sent = work_sent_rel_dict_worker_j[sentence_id]

                                work_sent_rel_dict_worker_j_sent_rel = work_sent_rel_dict_worker_j_sent[relation]
                                #print worker_i,worker_j,sentence_id,relation
                                numerator += sqs[sentence_id] * (work_sent_rel_dict_worker_i_sent[relation] *
                                                                 work_sent_rel_dict_worker_j_sent_rel)
                                denominator += sqs[sentence_id] * work_sent_rel_dict_worker_j_sent_rel

                        if denominator > 0:
                            rqs_numerator[relation] += wqs[worker_i] * wqs[worker_j] * numerator / denominator
                            rqs_denominator[relation] += wqs[worker_i] * wqs[worker_j]


        rqs = dict()
        for relation in relations:
            if rqs_denominator[relation] > SMALL_NUMBER_CONST:
                rqs[relation] = rqs_numerator[relation] / rqs_denominator[relation]

                # prevent division by zero by storing very small value instead
                if rqs[relation] < SMALL_NUMBER_CONST:
                    rqs[relation] = SMALL_NUMBER_CONST
            else:
                rqs[relation] = SMALL_NUMBER_CONST
        return rqs

    @staticmethod
    def run(results, config, max_delta = 0.001):
        '''
        iteratively run the CrowdTruth metrics
        '''

        judgments = results['judgments'].copy()
        units = results['units'].copy()

        # sent_work_rel_dict, work_sent_rel_dict, sent_rel_dict
        # to be done: change to use all vectors in one unit
        col = list(config.output.values())[0]
        sent_rel_dict = dict(units.copy()[col])

        def expanded_vector(worker, unit):
            '''
            expand the vector of a worker on a given unit
            '''
            vector = Counter()
            for rel in unit:
                if rel in worker:
                    vector[rel] = worker[rel]
                else:
                    vector[rel] = 0
            return vector

        # fill judgment vectors with unit keys
        for index, row in judgments.iterrows():
            # judgments.set_value(index, col, expandedVector(row[col], units.at[row['unit'], col]))
            judgments.at[index, col] = expanded_vector(row[col], units.at[row['unit'], col])

        sent_work_rel_dict = judgments[['unit', 'worker', col]].copy().groupby('unit')
        sent_work_rel_dict = {name : group.set_index('worker')[col].to_dict() \
                                for name, group in sent_work_rel_dict}

        work_sent_rel_dict = judgments[['worker', 'unit', col]].copy().groupby('worker')
        work_sent_rel_dict = {name : group.set_index('unit')[col].to_dict() \
                                for name, group in work_sent_rel_dict}

        #initialize data structures
        sqs_list = list()
        wqs_list = list()
        wwa_list = list()
        wsa_list = list()
        rqs_list = list()

        sqs = dict((sentence_id, 1.0) for sentence_id in sent_work_rel_dict)
        wqs = dict((worker_id, 1.0) for worker_id in work_sent_rel_dict)
        wwa = dict((worker_id, 1.0) for worker_id in work_sent_rel_dict)
        wsa = dict((worker_id, 1.0) for worker_id in work_sent_rel_dict)

        sqs_list.append(sqs.copy())
        wqs_list.append(wqs.copy())
        wwa_list.append(wwa.copy())
        wsa_list.append(wsa.copy())

        # initialize RQS depending on whether or not it is an open ended task
        rqs = dict()
        if not config.open_ended_task:
            rqs_keys = list(sent_rel_dict[list(sent_rel_dict.keys())[0]].keys())
            for relation in rqs_keys:
                rqs[relation] = 1.0
        else:
            for sentence_id in sent_rel_dict:
                for relation in sent_rel_dict[sentence_id]:
                    rqs[relation] = 1.0
        rqs_list.append(rqs.copy())

        sqs_len = len(list(sqs.keys())) * 1.0
        wqs_len = len(list(wqs.keys())) * 1.0
        rqs_len = len(list(rqs.keys())) * 1.0

        # compute metrics until stable values
        iterations = 0
        while max_delta >= 0.001:
            sqs_new = dict()
            wqs_new = dict()
            wwa_new = dict()
            wsa_new = dict()

            avg_sqs_delta = 0.0
            avg_wqs_delta = 0.0
            avg_rqs_delta = 0.0
            max_delta = 0.0

            # pdb.set_trace()

            if not config.open_ended_task:
                # compute relation quality score (RQS)
                rqs_new = Metrics.relation_quality_score(list(rqs.keys()), work_sent_rel_dict, \
                                                sqs_list[len(sqs_list) - 1], \
                                                wqs_list[len(wqs_list) - 1])
                for rel, _ in rqs_new.items():
                    max_delta = max(max_delta, abs(rqs_new[rel] - rqs_list[len(rqs_list) - 1][rel]))
                    avg_rqs_delta += abs(rqs_new[rel] - rqs_list[len(rqs_list) - 1][rel])
                avg_rqs_delta /= rqs_len

            # compute sentence quality score (SQS)
            for sent_id, _ in sent_work_rel_dict.items():
                sqs_new[sent_id] = Metrics.sentence_quality_score(sent_id, sent_work_rel_dict, \
                                                              wqs_list[len(wqs_list) - 1], \
                                                              rqs_list[len(rqs_list) - 1])
                max_delta = max(max_delta, abs(sqs_new[sent_id] - sqs_list[len(sqs_list) - 1][sent_id]))
                avg_sqs_delta += abs(sqs_new[sent_id] - sqs_list[len(sqs_list) - 1][sent_id])
            avg_sqs_delta /= sqs_len

            # compute worker quality score (WQS)
            for worker_id, _ in work_sent_rel_dict.items():
                wwa_new[worker_id] = Metrics.worker_worker_agreement(worker_id, \
                                        work_sent_rel_dict, sent_work_rel_dict, \
                                        wqs_list[len(wqs_list) - 1], sqs_list[len(sqs_list) - 1], \
                                        rqs_list[len(rqs_list) - 1])
                wsa_new[worker_id] = Metrics.worker_sentence_agreement(worker_id, sent_rel_dict, \
                                        work_sent_rel_dict, sqs_list[len(sqs_list) - 1], \
                                        rqs_list[len(rqs_list) - 1])
                wqs_new[worker_id] = wwa_new[worker_id] * wsa_new[worker_id]
                max_delta = max(max_delta, abs(wqs_new[worker_id] - wqs_list[len(wqs_list) - 1][worker_id]))
                avg_wqs_delta += abs(wqs_new[worker_id] - wqs_list[len(wqs_list) - 1][worker_id])
            avg_wqs_delta /= wqs_len

            # save results for current iteration
            sqs_list.append(sqs_new.copy())
            wqs_list.append(wqs_new.copy())
            wwa_list.append(wwa_new.copy())
            wsa_list.append(wsa_new.copy())
            if not config.open_ended_task:
                rqs_list.append(rqs_new.copy())
            iterations += 1

            # reconstruct sent_rel_dict with worker scores
            new_sent_rel_dict = dict()
            for sent_id, rel_dict in sent_rel_dict.items():
                new_sent_rel_dict[sent_id] = dict()
                for relation, _ in rel_dict.items():
                    new_sent_rel_dict[sent_id][relation] = 0.0
            for work_id, srd in work_sent_rel_dict.items():
                wqs_work_id = wqs_new[work_id]
                for sent_id, rel_dict in srd.items():
                    for relation, score in rel_dict.items():
                        new_sent_rel_dict[sent_id][relation] += score * wqs_work_id
            # pdb.set_trace()
            sent_rel_dict = new_sent_rel_dict

            logging.info(str(iterations) + " iterations; max d= " + str(max_delta) + \
                        " ; wqs d= " + str(avg_wqs_delta) + "; sqs d= " + str(avg_sqs_delta) + \
                        "; rqs d= " + str(avg_rqs_delta))

        srs = Counter()
        for sentence_id in sent_rel_dict:
            srs[sentence_id] = Counter()
            for relation in sent_rel_dict[sentence_id]:
                srs[sentence_id][relation] = Metrics.sentence_relation_score(sentence_id, \
                                            relation, sent_work_rel_dict, \
                                            wqs_list[len(wqs_list) - 1])

        srs_initial = Counter()
        for sentence_id in sent_rel_dict:
            srs_initial[sentence_id] = Counter()
            for relation in sent_rel_dict[sentence_id]:
                srs_initial[sentence_id][relation] = Metrics.sentence_relation_score(sentence_id, \
                                                    relation, sent_work_rel_dict, wqs_list[0])

        results['units']['uqs'] = pd.Series(sqs_list[-1])
        results['units']['unit_annotation_score'] = pd.Series(srs)
        results['workers']['wqs'] = pd.Series(wqs_list[-1])
        if not config.open_ended_task:
            results['annotations']['aqs'] = pd.Series(rqs_list[-1])

        results['units']['uqs_initial'] = pd.Series(sqs_list[1])
        results['units']['unit_annotation_score_initial'] = pd.Series(srs_initial)
        results['workers']['wqs_initial'] = pd.Series(wqs_list[1])
        if not config.open_ended_task:
            results['annotations']['aqs_initial'] = pd.Series(rqs_list[1])
        return results
