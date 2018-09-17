#pylint: disable=W0223

"""
Module used to process and load the input files to be evaluated with the CrowdTruth metrics.
"""

import os

import logging
import datetime
from collections import Counter, OrderedDict
import dateparser

import pandas as pd

from crowdtruth.models.worker import Worker
from crowdtruth.models.unit import Unit
from crowdtruth.models.job import Job
from crowdtruth.configuration import DefaultConfig
from crowdtruth.crowd_platform import *




# create an ordered counter so that we can maintain
# the position of tags in the order they were annotated
class OrderedCounter(Counter, OrderedDict):
    """ Instantiates an ordered counter. """
    pass

def create_ordered_counter(ordered_counter, annotation_vector):
    """ Instantiates an ordered counter from a given annotation vector. """
    for relation in annotation_vector:
        if relation not in ordered_counter:
            ordered_counter.update({relation: 0})
    return ordered_counter

def validate_timestamp_field(date_string, date_format):
    """ Validates the time columns (started time and submitted time) in input files. """

    try:
        date_obj = datetime.datetime.strptime(date_string, date_format)
        print(date_obj)
    except ValueError:
        raise ValueError('Incorrect date format')

def get_file_list(directory):
    """ List the files in the directry given as argument. """
    filelist = []

    # go through all files in this folder
    for file in os.listdir(directory):
        # if it is a folder scan it
        if os.path.isdir(directory+'/'+file):
            sublist = get_file_list(directory+'/'+file)
            sublist_length = len(sublist)
            if sublist_length:
                filelist.append(sublist)

        # if it is a csv file open it
        if file.endswith('.csv') and file != 'groundtruth.csv':
            filelist.append(file)
    return filelist

def list_files(kwargs, results, config):
    """ Creates a list of files to be processed. """
    files = []
    directory = ""
    if 'data_frame' in kwargs:
        res, config = process_file(kwargs['data_frame'], config)
        for value in res:
            results[value].append(res[value])
        return results
    elif 'file' in kwargs and kwargs['file'].endswith('.csv'):
        files = [kwargs['file']]
    elif 'directory' in kwargs:
        directory = kwargs['directory']
        files = get_file_list(directory)
        logging.info('Found ' + str(len(files)) + ' files')
    else:
        raise ValueError('No input was provided')

    for file in files:
        if 'directory' in locals() and directory != "":
            logging.info("Processing " + file)
            file = directory + "/" + file

        judgments = pd.read_csv(file)#, encoding=result['encoding'])
        res, config = process_file(judgments, config, filename=file)
        for value in res:
            results[value].append(res[value])

    return results

def load(**kwargs):
    """ Loads the input files. """

    # placeholder for aggregated results
    results = {
        'jobs' : [],
        'units' : [],
        'workers' : [],
        'judgments' : [],
        'annotations' : []
        }

    if 'config' not in kwargs:
        config = DefaultConfig()
    else:
        logging.info('Config loaded')
        config = kwargs['config']

    results = list_files(kwargs, results, config)
    for value in results:
        results[value] = pd.concat(results[value])


    # workers and annotations can appear across jobs, so we have to aggregate those extra
    results['workers'] = results['workers'].groupby(results['workers'].index).agg({
        'unit' : 'sum',
        'judgment' : 'sum',
        'job' : 'count',
        'duration' : 'mean'
        })

    # aggregate annotations
    results['annotations'] = results['annotations'].groupby(results['annotations'].index).sum()

    return results, config

def remove_empty_rows(config, judgments):
    """ handle rows where the worker did not give an answer (AMT issue) """

    # if config keeps empty rows, add NONE placehoder token
    if not config.remove_empty_rows:
        for col in config.outputColumns:
            for idx in range(len(judgments[col])):
                if (pd.isnull(judgments[col][idx]) or
                        judgments[col][idx] is None or
                        judgments[col][idx] == '' or
                        judgments[col][idx] == 'nan'):
                    logging.info('judgments[' + str(idx) + '][' + col + '] is None')
                    judgments.at[idx, col] = config.none_token
    # remove empty rows
    else:
        empty_rows = set()
        for col in config.outputColumns:
            empty_rows = empty_rows.union(judgments[pd.isnull(judgments[col]) == True].index)
            empty_rows = empty_rows.union(judgments[judgments[col] == 'nan'].index)
        for col in config.outputColumns:
            judgments = judgments[pd.isnull(judgments[col]) == False]
            judgments = judgments[judgments[col] != 'nan']
        judgments = judgments.reset_index(drop=True)
        count_empty_rows = len(empty_rows)
        if count_empty_rows > 0:
            if count_empty_rows == 1:
                logging.warning(str(count_empty_rows) + " row with incomplete information in "
                                "output columns was removed.")
            else:
                logging.warning(str(count_empty_rows) + " rows with incomplete information in "
                            "output columns were removed.")
    return judgments

def remove_single_judgment_units(judgments):
    """ remove units with just 1 judgment """
    units_1work = judgments.groupby('unit').filter(lambda x: len(x) == 1)["unit"]
    judgments = judgments[~judgments['unit'].isin(units_1work)]
    judgments = judgments.reset_index(drop=True)
    no_units_1work = len(units_1work)
    if no_units_1work > 0:
        if no_units_1work == 1:
            logging.warning(str(no_units_1work) + " Media Unit that was annotated by only"
                            " 1 Worker was omitted, since agreement cannot be calculated.")
        else:
            logging.warning(str(no_units_1work) + " Media Units that were annotated by only"
                            " 1 Worker were omitted, since agreement cannot be calculated.")
    return judgments

def make_output_cols_safe_keys(config, judgments):
    """ make output values safe keys """
    for col in config.output.values():
        if isinstance(judgments[col].iloc[0], dict):
            logging.info("Values stored as dictionary")
            if config.open_ended_task:
                judgments[col] = judgments[col].apply(lambda x: OrderedCounter(x))
            else:
                judgments[col] = judgments[col].apply(lambda x: create_ordered_counter( \
                                 OrderedCounter(x), config.annotation_vector))
        else:
            logging.info("Values not stored as dictionary")
            if config.open_ended_task:
                judgments[col] = judgments[col].apply(lambda x: OrderedCounter( \
                                                      x.split(config.annotation_separator)))
            else:
                judgments[col] = judgments[col].apply(lambda x: create_ordered_counter( \
                                 OrderedCounter(x.split(config.annotation_separator)), \
                                 config.annotation_vector))
    return judgments


def add_missing_values(config, units):
    """ Adds missing vector values if is a closed task """
    for col in config.output.values():
        try:
            # openended = config.open_ended_task
            for idx in list(units.index):
                for relation in config.annotation_vector:
                    if relation not in units[col][idx]:
                        units[col][idx].update({relation : 0})
            return units
        except AttributeError:
            continue
def aggregate_annotations(config, judgments):
    """ Aggregates annotations and adds judgments stats. """
    annotations = pd.DataFrame()
    for col in config.output.values():
        judgments[col+'.count'] = judgments[col].apply(lambda x: sum(x.values()))
        judgments[col+'.unique'] = judgments[col].apply(lambda x: len(x))
        res = pd.DataFrame(judgments[col].apply(lambda x: \
              pd.Series(list(x.keys())).value_counts()).sum(), columns=[col])
        annotations = pd.concat([annotations, res], axis=0)
    return annotations, judgments

def process_file(judgments, config, filename=""):
    """ Processes input files with the given configuration """

    platform = get_platform(judgments)

    if platform is False:
        logging.info("Custom crowdsourcing platform!")
        no_of_columns = len(config.customPlatformColumns)
        if no_of_columns != 5:
            logging.warning("The following column names are required: judgment id, "
                            "unit id, worker id, start time, submit time")
            raise ValueError('No custom platform configuration was provided')
        else:

            platform = {
                #'id'       : 'custom',
                config.customPlatformColumns[0] : 'judgment',
                config.customPlatformColumns[1] : 'unit',
                config.customPlatformColumns[2] : 'worker',
                config.customPlatformColumns[3] : 'started',
                config.customPlatformColumns[4] : 'submitted'
            }


    # we must establish which fields were part of the input data and which are output judgments
    # if there is a config, check if there is a definition of which fields to use
    #config = []
    # else use the default and select them automatically
    config = get_column_types(judgments, config)

    # allow customization of the judgments
    judgments = config.processJudgments(judgments)

    # handle empty rows
    judgments = remove_empty_rows(config, judgments)

    # update the config after the preprocessing of judgments
    config = get_column_types(judgments, config)

    all_columns = dict(list(config.input.items()) + list(config.output.items()) \
                       + list(platform.items()))
    # allColumns = dict(config.input.items() | config.output.items() | platform.items())
    judgments = judgments.rename(columns=all_columns)

    # remove columns we don't care about
    judgments = judgments[list(all_columns.values())]

    if filename != "":
        judgments['job'] = filename.split('.csv')[0]
    else:
        judgments['job'] = "pd.DataFrame"

    # make output values safe keys
    judgments = make_output_cols_safe_keys(config, judgments)

    # remove units with just 1 judgment
    judgments = remove_single_judgment_units(judgments)

    judgments['started'] = judgments['started'].apply(lambda x: dateparser.parse(str(x)))
    judgments['submitted'] = judgments['submitted'].apply(lambda x: dateparser.parse(str(x)))
    judgments['duration'] = judgments.apply(lambda row: (row['submitted'] - row['started']).seconds,
                                            axis=1)

    #
    # aggregate units
    #
    units = Unit.aggregate(judgments, config)

    #
    # aggregate annotations
    # i.e. output columns
    #
    annotations, judgments = aggregate_annotations(config, judgments)

    #
    # aggregate workers
    #
    workers = Worker.aggregate(judgments, config)

    #
    # aggregate job
    #
    job = Job.aggregate(units, judgments, config)

    # Clean up judgments
    # remove input columns from judgments
    output_cols = [col for col in judgments.columns.values \
                    if col.startswith('output') or col.startswith('metric')]
    judgments = judgments[output_cols + list(platform.values()) + ['duration', 'job']]

    # set judgment id as index
    judgments.set_index('judgment', inplace=True)

    # add missing vector values if closed task
    units = add_missing_values(config, units)

    return {
        'jobs' : job,
        'units' : units,
        'workers' : workers,
        'judgments' : judgments,
        'annotations' : annotations,
        }, config
