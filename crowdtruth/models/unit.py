class Unit():


    @staticmethod
    def aggregate(judgments, config):
        """ aggregate the judgments of a unit """
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
        """ count the number of annotations for each unit """
        for col in config.output.values():
            row[col+'.unique_annotations'] = len(row[col])
            row[col+'.annotations'] = sum(row[col].values())
        return row
