"""
Job initialization.
"""

class Job():
    """
    Performs general statistics over the crowdsourcing jobs.
    """

    @staticmethod
    def aggregate(units, judgments, config):
        """
        Aggregates information about the total number of units, total number of judgments,
        total number of workers that provided annotations and the total duration of the job.

        Args:
            units: Units contained in the job.
            judgments: Judgments contained in the job.
            config: Job configuration as provided as input for the metrics.

        Returns:
            A dataframe of one row that stores general stats on the crowdsourcing jobs.
        """
        agg = {
            'unit' : 'nunique',
            'judgment' : 'nunique',
            'worker' : 'nunique',
            'duration' : 'mean'
        }
        job = judgments.groupby('job').agg(agg)

        # compute job runtime
        runtime = (max(judgments['submitted']) - min(judgments['started']))
        job['runtime'] = runtime #float(runtime.days) * 24 + float(runtime.seconds) / 3600
        job['runtime.per_unit'] = job['runtime'] / job['unit']
        job['judgments.per.worker'] = job['judgment'] / job['worker']

        metrics = ['unique_annotations', 'annotations']
        for metric in metrics:
            for col in config.output.values():
                # aggregate unit metrics
                job[col+'.'+metric] = units[col+'.'+metric].mean()

        job = job.reindex(sorted(job.columns), axis=1)

        return job
