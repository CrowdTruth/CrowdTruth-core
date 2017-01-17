from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
import controllers.inputController as ic
import controllers.outputController as oc
import sys,os
from datetime import datetime
import pandas as pd
import numpy as np
import multiprocessing as mp


# define our default configuration options
defaults = init_defaults('crowdtruth')
defaults['crowdtruth']['debug'] = False
defaults['crowdtruth']['some_param'] = 'some value'

# define any hook functions here



# define the application class
class CrowdTruth(CementApp):
    class Meta:
        label = 'CrowdTruth'
        config_defaults = defaults
        extensions = ['json', 'yaml']







def scanDirectory(directory=''):
    root = os.getcwd()
    files = os.listdir(root+directory)
    app.log.debug("Found directory "+root+directory)
    print 'Directory:',directory


    results = {
        #'collections' : {},
        'jobs' : [],
        'units' : [],
        'workers' : [],
        'judgments' : [],
        'annotations' : []
        }

    if os.path.exists(root+directory+'/config.py'):
        sys.path.append(root+directory)
        from config import Configuration
        config = Configuration()
        config.custom = True
        print 'Loaded configuration for',config.name


    # go through all files in this folder
    for f in files:

        # if it is a folder scan it
        if os.path.isdir(root+directory+'/'+f):
            scanDirectory(directory+'/'+f)
        
        # if it is a configuration fole
        elif f == 'settings.ini':
            print 'found settings in', directory+'/'+f

        # if it is a csv file open it
        elif f.endswith('.csv'):
            # open csv
            res = ic.processFile(root, directory, f, config)
            for x in res:
                results[x].append(res[x])

    if len(results['jobs']) > 0:

        for x in results:
            results[x] = pd.concat(results[x])

        # workers and annotations can appear across jobs, so we have to aggregate those extra
        results['workers'] = results['workers'].groupby(results['workers'].index).agg({
            'unit' : 'sum',
            'judgment' : 'sum',
            'job' : 'count',
            'duration' : 'mean',
            'metrics.worker.agreement' : 'mean'
            })

        #results['annotations'] = results['annotations'].groupby(results['annotations'].index).sum()
        cols = [x for x in results['annotations'].columns.values if x.startswith('output')]
#       print results['annotations'].columns.values

        '''
        # todo: re enable
        results['correlations'] = pd.DataFrame()
        for col in cols:
            c = col.replace('output.','')
            results['annotations'][col].apply(lambda x: str(x))
            # corr freq
            answers = results['annotations'][col].value_counts().keys()
            for a in answers:
                results['correlations'][c+'.'+a] = results['annotations'][col].apply(lambda x: 1 if x == a else 0)

#        results['correlations'] = results['correlations'].corr(method='pearson')
#        results['correlations'] = results['correlations'].sort_index(axis=1)


#        print results['correlations'].head()
        
        '''

        results['annotations'] = results['annotations'].groupby(cols).count().reset_index()
        
        # How many times person a meets person b is described by the following (s.t. a < b)


        # DataFrames corr() function calculates pairwise correlations using specified 
        # algorithm: 'peason, 'kendall', and 'spearman' are supported.
        # Correlations are returned in a new DataFrame instance (corr_df below).
        #likert_corr_df = likert.corr(method='pearson')
        #likert_corr_df.to_csv(wd+'/results/likert_correlations.csv', sep=',')


        # add customized results
        if config.custom:
            results = config.customizeResults(results)

        oc.saveResults(root, directory, results)

        #pc.processFeatures(directory)
        if os.path.exists(root+directory+'/config.pyc'):
            os.remove(root+directory+'/config.pyc')


with CrowdTruth() as app:

    # track execution time
    startTime = datetime.now()

    # add arguments to the parser
    app.args.add_argument('-f', '--foo', action='store', metavar='STR',
                          help='the notorious foo option')

    # log stuff
    app.log.debug("About to run my myapp application!")

    # run the application
    app.run()

    # continue with additional application logic
    #if app.pargs.foo:
    #    app.log.info("Received option: foo => %s" % app.pargs.foo)

    # verify that we have something to do
    scanDirectory()

    app.log.info('Finished in ' + str(datetime.now() - startTime))
    
    app.close()
