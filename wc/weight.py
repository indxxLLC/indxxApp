import csv
import uuid
import pandas as pd

# read and write csv files
with open('C:/python/wc/staticfiles/upload/Copy of Weight Calculation_Sample.csv','r') as r_csvfile:
	with open('C:/python/wc/staticfiles/upload/weight.csv','w',newline='') as w_csvfile:
		dict_reader = csv.DictReader(r_csvfile,delimiter=',')
		#add new column with existing
		#row_count = sum(1 for row in dict_reader)
		dict_reader1 = dict_reader
		fieldnames = dict_reader.fieldnames + ['weight']
		writer_csv = csv.DictWriter(w_csvfile,fieldnames,delimiter=',')
		writer_csv.writeheader()
		
		df = pd.read_csv('C:/python/wc/staticfiles/upload/Copy of Weight Calculation_Sample.csv')
		row_count = len(df.axes[0])

		for row in dict_reader:
			row['weight'] = 100/row_count
			writer_csv.writerow(row)