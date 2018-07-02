#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:40:44 2018

@author: oanainel
"""

import pandas as pd
import itertools as it
import random
import os, sys

def get_uniq_unit_ids(df, unit_id_field):
    unique_unit_ids = df[unit_id_field].unique()
    return unique_unit_ids

def get_no_work_unit_id(df, unit_id, unit_id_field):
    subset_unit_id = df[df[unit_id_field] == unit_id]
    return (len(subset_unit_id), subset_unit_id)

def count_bits(number, n_bits):
    ret = 0
    bit_pos = []
    for i in xrange(0, n_bits):
        if (1 << i) & number != 0:
            ret += 1
            bit_pos.append(i)
    return (ret, bit_pos)
 
def gen_all_k_combinations(k, num_size):
    result = []
    for i in xrange(1, 2**num_size):
        bit_count, bit_pos = count_bits(i, num_size)
        if bit_count == k:
            result.append(bit_pos)
    return result

def gen_all_worker_combinations(subset_size, count, subset_unit_id, worker_id_field):
    combinations = gen_all_k_combinations(subset_size, count)
    final_result = []
    for comb in combinations:
        crnt_workers = []
        for j in xrange(0, len(comb)):
            crnt_workers.append(subset_unit_id[worker_id_field].iloc[comb[j]])
        final_result.append(crnt_workers)
    return final_result

def get_all_unit_combinations(unit_dict):
    sorted_unit_dict = sorted(unit_dict)
    combinations = it.product(*(unit_dict[unit_id] for unit_id in sorted_unit_dict))
    print(list(combinations))

def my_product(dicts):
    units, comb_of_workers = zip(*dicts.items())
    return [dict(zip(units, x)) for x in it.product(*comb_of_workers)]

def pick_random_worker_set(worker_sets):
    return random.choice(worker_sets)


def create_analysis_files(dataset_file, max_no_workers, max_runs, storing_folder, unit_id_field, worker_id_field):
    dataset = pd.read_csv(dataset_file)
    unique_unit_ids = get_uniq_unit_ids(dataset, unit_id_field)

    for subset_size in xrange(3, max_no_workers + 1):
        workers_directory = storing_folder + str(subset_size) + "workers"
        if not os.path.exists(workers_directory):
            os.makedirs(workers_directory)
            
        map_unit_id_combinations = {}
        for unit_id in xrange(0, len(unique_unit_ids)):
            (count, subset_unit_id) = get_no_work_unit_id(dataset, unique_unit_ids[unit_id], unit_id_field)
            combinations = gen_all_worker_combinations(subset_size, count, subset_unit_id, worker_id_field)
            map_unit_id_combinations[unique_unit_ids[unit_id]] = combinations

        for run_no in xrange(0, max_runs + 1):
            unit_worker_set = {}
            for unit_id, worker_sets in map_unit_id_combinations.iteritems():
                unit_worker_set[unit_id] = pick_random_worker_set(worker_sets)
            
            df_subset_size = pd.DataFrame()
            for unit_id, worker_set in unit_worker_set.iteritems():
                df_subset = dataset[(dataset[unit_id_field] == unit_id) & (dataset[worker_id_field].isin(worker_set))]
                frames = [df_subset_size, df_subset]
                df_subset_size = pd.concat(frames)
            
            df_subset_size.to_csv(workers_directory + "/run_" + str(run_no) + ".csv", index=False)
            

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    if len(argv) < 6:
        print('Usage: python replication_experiment_wrt_workers.py dataset_filename max_no_workers max_runs storing_folder unit_id_field, worker_id_field')
    else:
        create_analysis_files(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5]) 

if __name__ == '__main__':
    main()

