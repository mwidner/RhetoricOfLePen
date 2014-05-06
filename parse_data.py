'''
For Cécile Alduy's Rhetoric of LePen project
Read in a series of CSV files with metadata describing corpus
Count words in each text file
Output CSV of word frequencies with metadata

Mike Widner <mikewidner@stanford.edu>
'''
import csv
import collections
import sys
import string
import numpy as np
import pandas as pd

# list of files holding metadata about our texts
metadata = ['JMLP_discours.csv',
			'MLP_discours.csv',
			'JMLP_radio.csv',
			'MLP_radio.csv',
			'JMLP_tv.csv',
			'MLP_tv.csv']
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
corpora = basedir + 'corpora/'

# Add punctuation that appears in corpus to what we strip
string.punctuation += '…'

def count_words(filename):
	''' Count all the words in a file; return dictionary '''
	counts = collections.defaultdict(int)
	total = 0
	fh = open(filename, 'r', encoding='utf-8')
	for line in fh:
		words = line.split()
		for word in words:
			word = word.strip(string.punctuation).lower()
			counts[word] += 1
			total += 1
	return({'counts': counts, 'total': total})

def main(): 
	''' Loop through metadata files; count words in each text listed '''
	texts = []	# build up data for a DataFrame
	for filename in metadata:
		with open(basedir + filename, 'r', encoding='utf-8') as fh:
			try:
				reader = csv.DictReader(fh)
				# Columns: rid,filename,author,title,date,type,publication,place,length,collection,preparer
				for row in reader:
					# print("Processing " + row['filename'])
					ret = count_words(corpora + row['filename'])
					# row['data'] = pd.DataFrame([ret['counts']])
					row['data'] = pd.Series(ret['counts'])
					row['total'] = ret['total']
					texts.append(row)
			except FileNotFoundError as err:
				print("Missing file: " + basedir + row['filename'])
	df_texts = pd.DataFrame(texts)
	fh = open(basedir + 'words_of_interest', 'r')
	targets = []
	# df_words = pd.DataFrame(df_texts['data'])

	for t in fh:
		targets.append(t.rstrip())
	fh.close()
	# s_targets = pd.Series(targets)

	# most common words
	# df_texts.ix[i]['data'].order(ascending = False).head()

	# Probably not the best way to do this
	results = list()
	for i, s in df_texts['data'].iteritems():
		row = df_texts.ix[i]
		results.append(dict())
		results[i]['filename'] = row['filename']
		results[i]['total words'] = row['total']
		results[i]['author'] = row['author']
		results[i]['type'] = row['type']
		results[i]['filename'] = row['filename']
		results[i]['date'] = pd.to_datetime(row['date'], dayfirst=True, coerce=True)
		# print(date, author, genre, filename, tot)
		for word in targets:
			try:
				c = s.loc[word.lower()]
			except: 
				c = 0
			finally:
				results[i][word] = c / row['total']
				# print(word, c, c / tot)
	df_results = pd.DataFrame(results)
	df_results.to_csv('results.csv', encoding='latin-1')

if __name__ == '__main__':
	if sys.version_info[0] != 3:
	    print("This script requires Python 3")
	    exit(-1)
	main()