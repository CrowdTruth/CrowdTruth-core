"""
Worker initialization.
"""
class Worker():
    """
    Performs general statistics over the workers in the jobs.
    """

    @staticmethod
    def aggregate(judgments, config):
        """
        Aggregates information for each worker about the total number of jobs and units
        (s)he contributed to, the total number of judgments submitted, the total
        amount of time spent of annotating and the average number of annotations provided
        across all the units.

        Args:
            judgments: Judgments contained in the job.
            config: Job configuration as provided as input for the metrics.

        Returns:
            A dataframe containing all workers that contributed to the jobs and the
            statistics relevant for them.
        """
        workers = judgments.copy().groupby('worker')

        agg = {
            'job' : 'nunique',
            'unit' : 'nunique',
            'judgment' : 'nunique',
            'duration' : 'mean'
            }
        for col in config.output.values():
            agg[col+'.count'] = 'mean'

        workers = workers.agg(agg)

        return workers
