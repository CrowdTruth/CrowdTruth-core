from cement.core.foundation import CementApp
from cement.core import hook
from cement.utils.misc import init_defaults
import controllers.fileController as fc
import controllers.projectController as pc
import sys,os

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

            fc.processFile(root,directory,f)

        pc.processProject(directory)



with CrowdTruth() as app:
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
