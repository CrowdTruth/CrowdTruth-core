import datetime
import unit
import numpy as np
import itertools
import pandas as pd
from collections import Counter
from datetime import datetime
from collections import defaultdict
from pprint import pprint
import math
import logging

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
                
                try:
                    weighted_cosine = numerator / math.sqrt(denominator_i * denominator_j)
                except:
                    pdb.set_trace()
                sqs_numerator += weighted_cosine * wqs[worker_ids[worker_i]] * wqs[worker_ids[worker_j]]
                sqs_denominator += wqs[worker_ids[worker_i]] * wqs[worker_ids[worker_j]]
        
        if sqs_denominator < 0.0001:
          sqs_denominator = 0.0001
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
            
            for relation in worker_vector:
                worker_vector_relation = worker_vector[relation]
                sentence_vector_relation = sentence_vector[relation]

                numerator += rqs[relation] * worker_vector_relation * (sentence_vector_relation - worker_vector_relation)
                denominator_w += rqs[relation] * (worker_vector_relation * worker_vector_relation)
                denominator_s += rqs[relation] * ((sentence_vector_relation - worker_vector_relation) *
                                                  (sentence_vector_relation - worker_vector_relation))
            weighted_cosine = numerator / math.sqrt(denominator_w * denominator_s)
            wsa_numerator += weighted_cosine * sqs[sentence_id]
            wsa_denominator += sqs[sentence_id]
        if wsa_denominator < 0.0001:
            wsa_denominator = 0.0001
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
        
        wv = work_sent_rel_dict[worker_id]
        sentence_ids = list(work_sent_rel_dict[worker_id].keys())
        
        
        for sentence_id in sentence_ids:
            wv_sentence_id = wv[sentence_id]
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
                    wwa_numerator += weighted_cosine * wqs[other_worker_id] * sqs[sentence_id]
                    wwa_denominator += wqs[other_worker_id] * sqs[sentence_id]
        if wwa_denominator < 0.0001:
            # pdb.set_trace()
            wwa_denominator = 0.0001
        return wwa_numerator / wwa_denominator



    # Sentence - Relation Score
    @staticmethod
    def sentence_relation_score(sentence_id, relation, sent_work_rel_dict, wqs):
        srs_numerator = 0.0
        srs_denominator = 0.0
        
        worker_ids = sent_work_rel_dict[sentence_id]
        for worker_id in worker_ids:
            srs_numerator += worker_ids[worker_id][relation] * wqs[worker_id]
            srs_denominator += wqs[worker_id]
        # if srs_denominator < 0.0001:
        #  srs_denominator = 0.0001
        #    # pdb.set_trace()
        return srs_numerator / srs_denominator


    # Relation Quality Score
    @staticmethod
    def relation_quality_score(relations, work_sent_rel_dict, sqs, wqs):
        rqs_numerator = dict()
        rqs_denominator = dict()
        
        for relation in relations:
            rqs_numerator[relation] = 0.0
            rqs_denominator[relation] = 0.0
        
        worker_ids = work_sent_rel_dict.keys()
        for worker_i, work_sent_rel_dict_worker_i in work_sent_rel_dict.iteritems():
            #work_sent_rel_dict_worker_i = work_sent_rel_dict[worker_i]
            work_sent_rel_dict_i_keys = work_sent_rel_dict_worker_i.keys()
            for worker_j, work_sent_rel_dict_worker_j in work_sent_rel_dict.iteritems():
                #work_sent_rel_dict_worker_j = work_sent_rel_dict[worker_j]
                work_sent_rel_dict_j_keys = work_sent_rel_dict_worker_j.keys()
                
                #print worker_i, worker_j,np.intersect1d(np.array(work_sent_rel_dict[worker_i].keys()),np.array(work_sent_rel_dict[worker_j].keys()))
                if worker_i != worker_j and len(np.intersect1d(np.array(work_sent_rel_dict_i_keys),np.array(work_sent_rel_dict_j_keys))) > 0:
                        
                    for relation in relations:
                        numerator = 0.0
                        denominator = 0.0

                        for sentence_id, work_sent_rel_dict_worker_i_sent in work_sent_rel_dict_worker_i.iteritems():
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
            if rqs_denominator[relation] > 0:
                rqs[relation] = rqs_numerator[relation] / rqs_denominator[relation]
                
                # prevent division by zero by storing very small value instead
                if rqs[relation] < 0.0001:
                    rqs[relation] = 0.0001
            else:
                rqs[relation] = 1.0
        return rqs

    @staticmethod
    def run(results, config, max_delta = 0.001):
        
        judgments = results['judgments'].copy()
        units = results['units'].copy()

        #sent_work_rel_dict, work_sent_rel_dict, sent_rel_dict
        # TODO: change to use all vectors in one unit
        col = config.output.values()[0]
        sent_rel_dict = dict(units.copy()[col])

        def expandedVector(worker, unit):
            #print worker, unit
            vector = Counter()
            for rel in unit:
                if rel in worker:
                    vector[rel] = worker[rel]
                else:
                    vector[rel] = 0
            return vector

        # fill judgment vectors with unit keys
        for index,row in judgments.iterrows():
            judgments.set_value(index, col, expandedVector(row[col], units.at[row['unit'], col]))

        #print judgments.head()

        sent_work_rel_dict = judgments[['unit','worker',col]].copy().groupby('unit')
        sent_work_rel_dict = {name : group.set_index('worker')[col].to_dict() for name, group in sent_work_rel_dict}

        #print sent_work_rel_dict

        work_sent_rel_dict = judgments[['worker','unit',col]].copy().groupby('worker')
        work_sent_rel_dict = {name : group.set_index('unit')[col].to_dict() for name, group in work_sent_rel_dict}
#        print [i for i in list(sent_work_rel_dict)]
#        sent_work_rel_dict = {k : dict(sent_work_rel_dict[k]) for k in sent_work_rel_dict}

        #pprint(work_sent_rel_dict)

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
            rqs_keys = sent_rel_dict[sent_rel_dict.keys()[0]].keys()
            for relation in rqs_keys:
                rqs[relation] = 1.0
        else:
            for sentence_id in sent_rel_dict:
                for relation in sent_rel_dict[sentence_id]:
                    rqs[relation] = 1.0
        rqs_list.append(rqs.copy())

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
                rqs_new = Metrics.relation_quality_score(rqs.keys(), work_sent_rel_dict,
                                                 sqs_list[len(sqs_list) - 1],
                                                 wqs_list[len(wqs_list) - 1])
                for relation in rqs_new:
                    max_delta = max(max_delta, abs(rqs_new[relation] - rqs_list[len(rqs_list) - 1][relation]))
                    avg_rqs_delta += abs(rqs_new[relation] - rqs_list[len(rqs_list) - 1][relation])
                avg_rqs_delta /= len(rqs_new.keys()) * 1.0
            
            # compute sentence quality score (SQS)
            for sentence_id in sent_work_rel_dict:
                sqs_new[sentence_id] = Metrics.sentence_quality_score(sentence_id, sent_work_rel_dict,
                                                              wqs_list[len(wqs_list) - 1],
                                                              rqs_list[len(rqs_list) - 1])
                max_delta = max(max_delta, abs(sqs_new[sentence_id] - sqs_list[len(sqs_list) - 1][sentence_id]))
                avg_sqs_delta += abs(sqs_new[sentence_id] - sqs_list[len(sqs_list) - 1][sentence_id])
            avg_sqs_delta /= len(sqs_new.keys()) * 1.0
            
            # compute worker quality score (WQS)
            for worker_id in work_sent_rel_dict:
                wwa_new[worker_id] = Metrics.worker_worker_agreement(worker_id, work_sent_rel_dict, sent_work_rel_dict,
                                                             wqs_list[len(wqs_list) - 1],
                                                             sqs_list[len(sqs_list) - 1],
                                                             rqs_list[len(rqs_list) - 1])
                wsa_new[worker_id] = Metrics.worker_sentence_agreement(worker_id, sent_rel_dict, work_sent_rel_dict,
                                                               sqs_list[len(sqs_list) - 1],
                                                               rqs_list[len(rqs_list) - 1])
                wqs_new[worker_id] = wwa_new[worker_id] * wsa_new[worker_id]
                max_delta = max(max_delta, abs(wqs_new[worker_id] - wqs_list[len(wqs_list) - 1][worker_id]))
                avg_wqs_delta += abs(wqs_new[worker_id] - wqs_list[len(wqs_list) - 1][worker_id])
            avg_wqs_delta /= len(wqs_new.keys()) * 1.0
            
            # save results for current iteration
            sqs_list.append(sqs_new.copy())
            wqs_list.append(wqs_new.copy())
            wwa_list.append(wwa_new.copy())
            wsa_list.append(wsa_new.copy())
            if not config.open_ended_task:
                rqs_list.append(rqs_new.copy())
            iterations += 1 
            logging.info(str(iterations) + " iterations; max d= " + str(max_delta) + " ; wqs d= " + str(avg_wqs_delta) + "; sqs d= " + str(avg_sqs_delta) + "; rqs d= " + str(avg_rqs_delta))

            #if iterations == 1:
            #    break
        #pprint(sqs_list)
        #pprint(wqs_list)
        #pprint(rqs_list)
        
        srs = Counter()
        for sentence_id in sent_rel_dict:
            srs[sentence_id] = Counter()
            for relation in sent_rel_dict[sentence_id]:
                srs[sentence_id][relation] = Metrics.sentence_relation_score(sentence_id, relation, sent_work_rel_dict, wqs_list[len(wqs_list) - 1])
        
        srs_initial = Counter()
        for sentence_id in sent_rel_dict:
            srs_initial[sentence_id] = Counter()
            for relation in sent_rel_dict[sentence_id]:
                srs_initial[sentence_id][relation] = Metrics.sentence_relation_score(sentence_id, relation, sent_work_rel_dict, wqs_list[0])

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
