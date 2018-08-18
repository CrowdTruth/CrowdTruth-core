#pylint: disable=W0223

"""
Module used to process and load the input files to be evaluated with the CrowdTruth metrics.
"""

import os

import logging
import datetime

from collections import Counter, OrderedDict

import pandas as pd

from crowdtruth.models.worker import Worker
from crowdtruth.models.unit import Unit
from crowdtruth.models.job import Job
from crowdtruth.configuration import DefaultConfig




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


class Found(Exception):
    """ Exception. """
    pass

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
    if 'file' in kwargs and kwargs['file'].endswith('.csv'):
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
        res, config = process_file(file, config)
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
    """ remove rows where the worker did not give an answer (AMT issue) """
    empty_rows = set()
    for col in config.outputColumns:
        empty_rows = empty_rows.union(judgments[pd.isnull(judgments[col]) == True].index)
    for col in config.outputColumns:
        judgments = judgments[pd.isnull(judgments[col]) == False]
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

def process_file(filename, config):
    """ Processes input files with the given configuration """

    judgments = pd.read_csv(filename)#, encoding=result['encoding'])

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

    judgments = remove_empty_rows(config, judgments)
    # allow customization of the judgments
    judgments = config.processJudgments(judgments)

    # update the config after the preprocessing of judgments
    config = get_column_types(judgments, config)

    all_columns = dict(list(config.input.items()) + list(config.output.items()) \
                       + list(platform.items()))
    # allColumns = dict(config.input.items() | config.output.items() | platform.items())
    judgments = judgments.rename(columns=all_columns)

    # remove columns we don't care about
    judgments = judgments[list(all_columns.values())]

    judgments['job'] = filename.split('.csv')[0]

    # make output values safe keys
    judgments = make_output_cols_safe_keys(config, judgments)

    judgments['started'] = judgments['started'].apply(lambda x: pd.to_datetime(str(x)))
    judgments['submitted'] = judgments['submitted'].apply(lambda x: pd.to_datetime(str(x)))
    judgments['duration'] = judgments.apply(lambda row: (row['submitted'] - row['started']).seconds,
                                            axis=1)

    # remove units with just 1 judgment
    judgments = remove_single_judgment_units(judgments)

    #
    # aggregate units
    #
    units = Unit.aggregate(judgments, config)

    for col in config.output.values():
        judgments[col+'.count'] = judgments[col].apply(lambda x: sum(x.values()))
        judgments[col+'.unique'] = judgments[col].apply(lambda x: len(x))


    #
    # aggregate workers
    #
    workers = Worker.aggregate(judgments, config)


    #
    # aggregate annotations
    # i.e. output columns
    #
    annotations = pd.DataFrame()
    for col in config.output.values():
        res = pd.DataFrame(judgments[col].apply(lambda x: \
              pd.Series(list(x.keys())).value_counts()).sum(), columns=[col])
        annotations = pd.concat([annotations, res], axis=0)

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


def get_platform(dframe):
    """ Get the crowdsourcing platform this file originates to """

    if dframe.columns.values[0] == '_unit_id':
        # CrowdFlower
        return {
            #'_platform'        : 'cf',
            '_id'           : 'judgment',
            '_unit_id'      : 'unit',
            '_worker_id'    : 'worker',
            '_started_at'   : 'started',
            '_created_at'   : 'submitted'
        }
    elif dframe.columns.values[0] == 'HITId':
        # Mturk
        return {
            #'id'       : 'amt',
            'AssignmentId'  : 'judgment',
            'HITId'         : 'unit',
            'WorkerId'      : 'worker',
            'AcceptTime'    : 'started',
            'SubmitTime'    : 'submitted'
        }
    return False

def configure_amt_columns(dframe, config):
    """ Configures AMT input and output columns. """
    config.input = {}
    config.output = {}

    if config.inputColumns:
        config.input = {c: 'input.'+c.replace('Input.', '') \
                        for c in dframe.columns.values if c in config.inputColumns}
    else:
        config.input = {c: 'input.'+c.replace('Input.', '') \
                        for c in dframe.columns.values if c.startswith('Input.')}

    # if config is specified, use those columns
    if config.outputColumns:
        config.output = {c: 'output.'+c.replace('Answer.', '') \
                         for c in dframe.columns.values if c in config.outputColumns}
    else:
        config.output = {c: 'output.'+c.replace('Answer.', '') \
                         for c in dframe.columns.values if c.startswith('Answer.')}
    return config.input, config.output

def configure_platform_columns(dframe, config):
    """ Configures FigureEight and custom platforms input and output columns. """
    config.input = {}
    config.output = {}

    if config.inputColumns:
        config.input = {c: 'input.'+c for c in dframe.columns.values \
                        if c in config.inputColumns}
    if config.outputColumns:
        config.output = {c: 'output.'+c for c in dframe.columns.values \
                         if c in config.outputColumns}
    return config.input, config.output

def configure_with_missing_columns(dframe, config):
    """ Identifies the type of the column based on naming """
    units = dframe.groupby('_unit_id')
    columns = [c for c in dframe.columns.values if c != 'clustering' and not c.startswith('_') \
                   and not c.startswith('e_') and not c.endswith('_gold') \
                   and not c.endswith('_reason') and not c.endswith('browser')]
    for colname in columns:
        try:
            for _, unit in units:
                unique = unit[colname].nunique()
                if unique != 1 and unique != 0:
                    raise Found
            if not config.inputColumns:
                config.input[colname] = 'input.'+colname

        except Found:
            if not config.outputColumns:
                config.output[colname] = 'output.'+colname

    return config

def get_column_types(dframe, config):
    """ return input and output columns """
    # returns a list of columns that contain are input content
    config.input = {}
    config.output = {}

    # get a dict of the columns with input content and the columns with output judgments
    # each entry matches [original column name]:[safestring column name]
    if dframe.columns.values[0] == 'HITId':
        # Mturk
        # if config is specified, use those columns
        config.input, config.output = configure_amt_columns(dframe, config)

        return config

    elif dframe.columns.values[0] == '_unit_id':

        # if a config is specified, use those columns
        config.input, config.output = configure_platform_columns(dframe, config)
        # if there is a config for both input and output columns, we can return those
        if config.inputColumns and config.outputColumns:
            return config

        # try to identify the input and output columns
        # this is the case if all the values in the column are identical
        # this is not failsafe but should give decent results without settings
        # it is best to make a settings.py file for a collection

        return configure_with_missing_columns(dframe, config)

    else:
        # unknown platform type

        # if a config is specified, use those columns
        config.input, config.output = configure_platform_columns(dframe, config)
        # if there is a config for both input and output columns, we can return those
        if config.inputColumns and config.outputColumns:
            return config
