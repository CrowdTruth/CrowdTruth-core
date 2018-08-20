"""
Module used to process information regarding the crowdsourcing platform.
"""
class Found(Exception):
    """ Exception. """
    pass

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
