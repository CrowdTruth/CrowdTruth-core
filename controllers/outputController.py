
import pandas as pd
import os


def saveResults(root, directory, results):
	filename = directory.replace('/', '-')
	writer = pd.ExcelWriter(root+directory+'/results'+filename+'.xlsx',options={'encoding':'cp1252'})
	for tab in results:
		#print 'Saving:',tab
		results[tab].to_excel(writer, tab)
	writer.save()
	print 'Saved: '+directory+'results'+filename+'.xlsx'