class DefaultConfig():
    """Define default configuration for cases when users do not provide a custom one"""

    name = '' # collection name
    inputColumns = [] # inputColumns to use
    outputColumns = [] # outputColumns to use
    customPlatformColumns = []
    open_ended_task = True
    annotation_vector = []

    units = []  # units to use
    workers = [] # workers to use
    jobs = [] # jobs to use

    csv_file_separator = ','
    annotation_separator = ','


    def processJudgments(self, judgments):
        """ Custom configuration of the judgments """
        return judgments

    def processResults(self, results, config=[]):
        """ Processing of the reuslts using the provided configuration """
        return results
