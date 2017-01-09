from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
import controllers.inputController as ic
import controllers.outputController as oc
import controllers.featureController as pc
import sys,os
from datetime import datetime
import pandas as pd
import numpy as np

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
            print 'csv:',f

            res = ic.processFile(root, directory, f)
            for x in res:
                results[x].append(res[x])


    for x in results:
        results[x] = pd.concat(results[x])

    # workers and annotations can appear across jobs, so we have to aggregate those extra
    results['workers'] = results['workers'].groupby(results['workers'].index).agg({
        'unit' : 'sum',
        'judgment' : 'sum',
        'job' : 'count',
        'duration' : 'mean'
        })

    results['annotations'] = results['annotations'].groupby(results['annotations'].index).sum().T
 

    oc.saveResults(results)

        #pc.processFeatures(directory)



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
