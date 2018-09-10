"""
Module used to configure the processing of the input files.
"""

class DefaultConfig():
    """ Defines default configuration for cases when users do not provide a custom one.

    Creates a class that lets us define how the input file will be processed:
        inputColumns: List of input columns from the .csv file, what the workers were shown.
        outputColumns: List of output columns with the answers from the workers.
        customPlatformColumns: List of columns that define standard annotation tasks, such as
                               judgment id, unit id, worker id, started time, submitted time.
                               This variable is used for custom input files (i.e., do not come
                               from AMT or FigureEight.)
        open_ended_task = Takes the value True if we deal with an open task and False othewise.
        annotation_vector = List of annotations from with the crowd can choose from. Only applicable
                            for closed tasks.
        units = List of units to be used.
        workers = List of workers to be used.
        jobs = List of jobs to be used.
        csv_file_separator = Column separator for the input csv files.
        annotation_separator = Separator for worker judgments. Default separator for judgments is ','
        processJudgments: Function that defines how the worker judgments wil be processed.
    """

    name = '' # collection name
    inputColumns = [] # inputColumns to use
    outputColumns = [] # outputColumns to use
    customPlatformColumns = []
    open_ended_task = True
    annotation_vector = []
    
    remove_empty_rows = True
    none_token = "NONE"

    units = []  # units to use
    workers = [] # workers to use
    jobs = [] # jobs to use

    csv_file_separator = ','
    annotation_separator = ','

    def processJudgments(self, judgments):
        """
        Defines how the worker judgments wil be processed.
        """
        return judgments
