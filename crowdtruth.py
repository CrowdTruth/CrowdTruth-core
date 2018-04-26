from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
import controllers.inputController as ic
import controllers.outputController as oc
import controllers.configController as cc
from models import *
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







def scanDirectory(directory='',root=''):
    if root == '':
        root = os.getcwd()
    files = os.listdir(root+directory)
    app.log.debug("Found directory "+root+directory)
    print 'Directory:',root,directory


    results = {
        #'collections' : {},
        'jobs' : [],
        'units' : [],
        'workers' : [],
        'judgments' : [],
        'annotations' : []
        }

    config = cc.getConfig(root, directory)


    # go through all files in this folder
    subdirectories = []
    for f in files:

        # if it is a folder scan it
        if os.path.isdir(root+directory+'/'+f):
            subdirectories.append(directory+'/'+f)

        # if it is a csv file open it
        elif f.endswith('.csv') and f <> 'groundtruth.csv':
            # open csv
            res = ic.processFile(root, directory, f, config)
            for x in res:
                results[x].append(res[x])



    # if jobs were found
    if len(results['jobs']) > 0:

        for x in results:
            results[x] = pd.concat(results[x])

        # workers and annotations can appear across jobs, so we have to aggregate those extra
        results['workers'] = results['workers'].groupby(results['workers'].index).agg({
            'unit' : 'sum',
            'judgment' : 'sum',
            'job' : 'count',
            'duration' : 'mean',
            'spam' : 'sum',
            'worker-cosine' : 'mean',
            'worker-agreement' : 'mean'
            })



        # aggregate annotations
        results['annotations'] = results['annotations'].groupby(results['annotations'].index).sum()
        

        #
        # compute correlations
        #
        # remove 'output.' from the annotation column names
        

        # How many times person a meets person b is described by the following (s.t. a < b)


        # DataFrames corr() function calculates pairwise correlations using specified 
        # algorithm: 'peason, 'kendall', and 'spearman' are supported.
        # Correlations are returned in a new DataFrame instance (corr_df below).
        #likert_corr_df = likert.corr(method='pearson')
        #likert_corr_df.to_csv(wd+'/results/likert_correlations.csv', sep=',')


        results = Metrics.run(results, config)

        # add customized results
        for c in config.output.items():
            results['units'][c[1]] = results['units'][c[1]].apply(lambda x: dict(x))

        # remove Counter for readability
        for col in config.output.values():
            results['judgments'][col] = results['judgments'][col].apply(lambda x: ','.join(x.keys()))


        results = config.processResults(results, config)

        oc.saveResults(root, directory, results)


    # remove config from system path
    if config.name:
        sys.path.remove(root+directory)
        del sys.modules['config']
    if os.path.exists(root+directory+'/config.pyc'):
        os.remove(root+directory+'/config.pyc')


    # dive into subdirectories
    for f in subdirectories:
        scanDirectory(directory+'/'+f,root)



with CrowdTruth() as app:

    # track execution time
    startTime = datetime.now()

    # add arguments to the parser
    app.args.add_argument('-d', '--dir', action='store', metavar='DIR',
                          help='Set root directory (provide absolute path)')

    # log stuff
    app.log.debug("About to run my myapp application!")

    # run the application
    app.run()

    # continue with additional application logic
    #
    if app.pargs.dir:
        scanDirectory(root=app.pargs.dir)
    else:
        scanDirectory()
    # verify that we have something to do




    app.log.info('Finished in ' + str(datetime.now() - startTime))
    
    app.close()
