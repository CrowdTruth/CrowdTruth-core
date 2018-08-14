import pandas as pd
import os


def save(results, config, directory=''):
	if directory == '':
		directory = os.getcwd()
	#filename = directory.replace('/', '-')
	writer = pd.ExcelWriter(directory+'/results.xlsx',options={'encoding':'cp1252'})

	# write data
	for tab in results:
		results[tab].to_excel(writer, tab)
	writer.save()
	print('Saved to: ', directory+'/results.xlsx')