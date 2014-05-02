# import nltk
# import matplotlib.pyplot as plt
import csv
# from pylab import *
# import pylab
# from operator import itemgetter, attrgetter
import collections
import sys
import string

# list of files holding metadata about our texts
metadata = ['JMLP_discours.csv',
			'MLP_discours.csv',
			'JMLP_radio.csv',
			'MLP_radio.csv',
			'JMLP_tv.csv',
			'MLP_tv.csv']
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
corpora = basedir + 'corpora/'

def count_words(filename):
	''' Count all the words in a file; return dictionary '''
	print('Counting ' + filename)
	counts = collections.defaultdict(int)
	total = 0
	fh = open(filename, 'r', encoding='utf-8')
	for line in fh:
		words = line.split()
		for word in words:
			word = word.strip(string.punctuation).lower()
			counts[word] += 1
			total += 1
	return(counts, total)

def main(): 
	''' Loop through metadata files; count words in each text listed '''
	all_counts = dict()
	for filename in metadata:
		with open(basedir + filename, 'r', encoding='utf-8') as fh:
			reader = csv.DictReader(fh)
			# Columns: rid,filename,author,title,date,type,publication,place,length,collection,preparer
			for row in reader:
				ret = count_words(corpora + row['filename'])
				all_counts[row['filename']] = dict()
				all_counts[row['filename']]['counts'] = ret[0]
				all_counts[row['filename']]['total'] = ret[1]
				# print(corpora + row['filename'], row['date'], row['title'])
	# fh = open(basedir + 'words_of_interest', 'r')

if __name__ == '__main__':
	if sys.version_info[0] != 3:
	    print("This script requires Python 3")
	    exit(-1)
	main()

# 1. read word list
# word_counts = basedir + 'wordcounts_all.csv'
# fh = open(basedir + 'words_of_interest', 'r')
# targets = []
# for t in fh:
# 	targets.append(t.rstrip())
# fh.close()
# word_counts = csv.DictReader(open(word_counts, 'r'))


# totals = dict()
# words = []
# for row in word_counts:
# 	if row['mot'] in targets:
# 		totals[row['mot']] = int(row['MLP total global'])
# 		# print '{"x":"' + row['mot'] + '", "y":' + row['MLP total global'] + '},'
# 		# totals.append(row['MLP total global'])
# 		# words.append(row['mot'])

# tots = collections.OrderedDict(sorted(totals.items(), key=lambda t: t[1], reverse=True))
# for key in tots.keys():
# 	print '{"x":"' + key + '", "y":' + str(tots[key]) + '},'

	# print key, tots[key]

# ind = pylab.arange(len(totals))
# width = 0.35
# ax = plt.subplot()
# ax.set_ylabel('Raw Frequency')
# # plt.xticks(ind + width / 2, words)
# bar1 = ax.bar(ind, totals, width, color = 'r')
# plt.plot(tots.values())
# plt.show()

# stacked bar charts of word totals across genres
# historical, grouped bar charts for years of genres, grouped by word


# 2. read metadata lists
# 3. parse metadata lists, build list of files
# 4. process files
#		a. clean
#		b. normalize?
#		c. chunk
# 5. count words
# 6. visualize w/ matplotlib