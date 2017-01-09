
import pandas as pd
import os


def saveResults(results):
	writer = pd.ExcelWriter('results.xlsx')
	for tab in results:
		print 'Saving:',tab
		results[tab].to_excel(writer, tab)
	writer.save()