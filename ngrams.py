'''
Read output from TreeTagger
filter based on desired parts of speech

Mike Widner <mikewidner@stanford.edu>
'''

# how many n-grams to find
TOT_NGRAMS = 500
# how frequent must an n-gram be for inclusion
FREQ_FILTER = 3
# minimum length of words to include
MIN_LENGTH = 3

import string
import nltk
import csv
import collections
import itertools
from nltk.corpus import PlaintextCorpusReader
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder

string.punctuation += "…"
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
corpus_root = basedir + 'corpora/years'
wordlists = PlaintextCorpusReader(corpus_root, ".*\.txt$")

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()

fh = open(basedir + 'stopwords.txt', 'r')
stopwords = fh.read()
fh.close()

def write_results(results, prefix):
	# Bigrams
	fh = open(basedir + 'results/' + prefix + '-bigrams.txt', 'w')
	for bigram in results['bigrams']:
		fh.write(' '.join(bigram) + "\n")
	fh.close()
	fh = csv.writer(open(basedir + 'results/' + prefix + '-bigram_prefix.csv', 'w', encoding='utf-8'), dialect='excel')
	fh.writerow(['first', 'second', 'likelihood_ratio'])
	for key in results['b_prefix']:
		for item in results['b_prefix'][key]:
			fh.writerow([key, item[0], item[1]])

	# Trigrams
	fh = open(basedir + 'results/' + prefix + '-trigrams.txt', 'w')
	for trigram in results['trigrams']:
		fh.write(' '.join(trigram) + "\n")
	fh.close()
	fh = csv.writer(open(basedir + 'results/' + prefix + '-trigram_prefix.csv', 'w', encoding='utf-8'))
	fh.writerow(['first', 'second', 'third', 'likelihood_ratio'])
	for key in results['t_prefix']:
		for item in results['t_prefix'][key]:
			fh.writerow([key, item[0], item[1], item[2]])

	# Freq Dist
	fh = csv.writer(open(basedir + 'results/' + prefix + '-fdist.csv', 'w', encoding='utf-8'), dialect='excel')
	fh.writerow(['word', 'raw_frequency'])
	for word in results['fdist'].keys():
		fh.writerow([word, results['fdist'][word]])

def analyze_text(text):
	words = [w.lower() for w in text 
				if w not in string.punctuation 
				and w not in stopwords
				and len(w) > MIN_LENGTH]

	fdist = nltk.FreqDist(words)

	# what follows could totally be generalized
	# Bigrams
	b_finder = BigramCollocationFinder.from_words(words)
	b_finder.apply_freq_filter(FREQ_FILTER)
	bigrams = b_finder.nbest(bigram_measures.pmi, TOT_NGRAMS)
	b_scored = b_finder.score_ngrams(bigram_measures.likelihood_ratio)
	b_prefix_keys = collections.defaultdict(list)
	for key, scores in b_scored:
		b_prefix_keys[key[0]].append((key[1], scores))

	# Trigrams
	t_finder = TrigramCollocationFinder.from_words(words)
	t_finder.apply_freq_filter(FREQ_FILTER)
	trigrams = t_finder.nbest(trigram_measures.pmi, TOT_NGRAMS)
	t_scored = t_finder.score_ngrams(trigram_measures.likelihood_ratio)
	t_prefix_keys = collections.defaultdict(list)
	for key, scores in t_scored:
		t_prefix_keys[key[0]].append((key[1], key[2], scores))

	return({'bigrams': bigrams, 'b_prefix': b_prefix_keys, 
			'trigrams': trigrams, 't_prefix': t_prefix_keys, 
			'fdist': fdist})

# Diachronic results
for filename in wordlists.fileids():
	year = int(filename.partition(".")[0])	# grab the year from the filename
	results = analyze_text(wordlists.words(fileids=[filename]))
	write_results(results, str(year))

# Synchronic results
results = analyze_text(wordlists.words())
write_results(results, "all")

