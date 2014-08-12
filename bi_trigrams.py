'''
Read output from a corpus of text files
Create bigrams, trigrams, and frequency distributions

See documentation here: http://www.nltk.org/howto/collocations.html

Mike Widner <mikewidner@stanford.edu>
'''

# how many n-grams to find
TOT_NGRAMS = 500
# how frequent must an n-gram be for inclusion
FREQ_FILTER = 3
# minimum character length of words to include
MIN_LENGTH = 4

import os
import csv
import nltk
import string
import itertools
import collections

from nltk.corpus import PlaintextCorpusReader
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder

string.punctuation += "…"
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
# corpusdir = basedir + 'corpora/years'
# resultsdir = basedir + 'results/by_year/'

corpusdir = basedir + 'corpora/authors/'
resultsdir = basedir + 'results/by_author/'

wordlists = PlaintextCorpusReader(corpusdir, ".*\.txt$")

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()

fh = open(basedir + 'stopwords.txt', 'r')
stopwords = fh.read()
fh.close()

def write_results(results, prefix):
	if not os.path.isdir(resultsdir):
		os.makedirs(resultsdir)

	# Bigrams
	fh = open(prefix + '-bigrams.txt', 'w')
	for bigram in results['bigrams']:
		fh.write(' '.join(bigram) + "\n")
	fh.close()
	fh = csv.writer(open(prefix + '-bigram_prefix.csv', 'w', encoding='utf-8'), dialect='excel')
	fh.writerow(['first', 'second', 'likelihood_ratio'])
	for key in results['b_prefix']:
		for item in results['b_prefix'][key]:
			fh.writerow([key, item[0], item[1]])

	# Trigrams
	fh = open(prefix + '-trigrams.txt', 'w')
	for trigram in results['trigrams']:
		fh.write(' '.join(trigram) + "\n")
	fh.close()
	fh = csv.writer(open(prefix + '-trigram_prefix.csv', 'w', encoding='utf-8'))
	fh.writerow(['first', 'second', 'third', 'likelihood_ratio'])
	for key in results['t_prefix']:
		for item in results['t_prefix'][key]:
			fh.writerow([key, item[0], item[1], item[2]])

	# Freq Dist
	fh = csv.writer(open(prefix + '-fdist.csv', 'w', encoding='utf-8'), dialect='excel')
	fh.writerow(['word', 'raw_frequency'])
	for word in results['fdist'].keys():
		fh.writerow([word, results['fdist'][word]])

def analyze_text(text):
	words = [w.lower() for w in text 
				if w not in string.punctuation 
				and len(w) >= MIN_LENGTH]

	fdist = nltk.FreqDist(words)

	# what follows could totally be generalized
	# Bigrams
	b_finder = BigramCollocationFinder.from_words(words)
	b_finder.apply_freq_filter(FREQ_FILTER)
	b_finder.apply_word_filter(lambda w: w in stopwords)
	bigrams = b_finder.nbest(bigram_measures.likelihood_ratio, TOT_NGRAMS)
	b_scored = b_finder.score_ngrams(bigram_measures.likelihood_ratio)
	b_prefix_keys = collections.defaultdict(list)
	for key, scores in b_scored:
		b_prefix_keys[key[0]].append((key[1], scores))

	# Trigrams
	t_finder = TrigramCollocationFinder.from_words(words)
	t_finder.apply_freq_filter(FREQ_FILTER)
	t_finder.apply_word_filter(lambda w: w in stopwords)
	trigrams = t_finder.nbest(trigram_measures.likelihood_ratio, TOT_NGRAMS)
	t_scored = t_finder.score_ngrams(trigram_measures.likelihood_ratio)
	t_prefix_keys = collections.defaultdict(list)
	for key, scores in t_scored:
		t_prefix_keys[key[0]].append((key[1], key[2], scores))

	return({'bigrams': bigrams, 'b_prefix': b_prefix_keys, 
			'trigrams': trigrams, 't_prefix': t_prefix_keys, 
			'fdist': fdist})

wc_fh = csv.writer(open(resultsdir + 'word_counts.csv', 'w', encoding='utf-8'))
wc_fh.writerow(['year', 'words'])
# Per file results
for filename in wordlists.fileids():
	year = filename.partition(".")[0]	# grab the year from the filename
	wc_fh.writerow([year, len(wordlists.words(fileids=[filename]))])
	results = analyze_text(wordlists.words(fileids=[filename]))
	write_results(results, resultsdir + year)

# Cumulative results
wc_fh.writerow(['all', len(wordlists.words())])
results = analyze_text(wordlists.words())
write_results(results, resultsdir + "all")