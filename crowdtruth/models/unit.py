"""
Unit initialization.
"""
class Unit():
    """
    Performs general statistics over the units in the jobs.
    """

    @staticmethod
    def aggregate(judgments, config):
        """
        Aggregates information for each unit in the job. For each unit we save the
        data that was used as input (in the crowdsourcing template), the job in which
        it appeared, the number of workers that annotated the unit and the total
        amount of time spent by the workers to annotate it.

        Args:
            judgments: Judgments contained in the job.
            config: Job configuration as provided as input for the metrics.

        Returns:
            A dataframe containing all units that appear in the jobs and the
            statistics relevant for them.
        """
        agg = {}
        for col in config.input.values():
            # for each input column the first value is taken.
            # all rows have the same value for each unit.
            agg[col] = 'first'
        for col in config.output.values():
            # each output column dict is summed
            agg[col] = 'sum'
        agg['job'] = 'first'
        agg['worker'] = 'count'
        agg['duration'] = 'mean'

        units = judgments.groupby('unit').agg(agg)

        #
        # get unit metrics
        #
        # for each vector in the unit get the unit metrics
        units = units.apply(lambda row: Unit.get_metrics(row, config), axis=1)

        # sort columns
        units = units.reindex(sorted(units.columns), axis=1)

        return units

    @staticmethod
    def get_metrics(row, config):
        """
        Counts the number of annotations and the number of unique annotations for each unit.
        """
        for col in config.output.values():
            row[col+'.unique_annotations'] = len(row[col])
            row[col+'.annotations'] = sum(row[col].values())
        return row
