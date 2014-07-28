'''
Read output from TreeTagger
filter based on desired parts of speech

Mike Widner <mikewidner@stanford.edu>
'''

# how many n-grams to find
TOT_NGRAMS = 50
# how frequent must the be
FREQ_FILTER = 3

import string
import nltk
import csv
from nltk.corpus import PlaintextCorpusReader
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder
from collections import defaultdict
# from nltk import TreeTagger

string.punctuation += "…"
string.punctuation = string.punctuation.replace("'", '')
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
corpus_root = basedir + 'corpora/years'
wordlists = PlaintextCorpusReader(corpus_root, ".*\.txt$")

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()

# bigrams = defaultdict(list)
# trigrams = defaultdict(list)
# fdists = defaultdict(dict)

fh = open(basedir + 'stopwords.txt', 'r')
stopwords = fh.read()
fh.close()

def write_results(bigrams, trigrams, fdist, prefix):
	fh = open(basedir + 'results/' + prefix + '-bigrams.txt', 'w')
	for bigram in bigrams:
		fh.write(' '.join(bigram) + "\n")
	fh.close()
	fh = open(basedir + 'results/' + prefix + '-trigrams.txt', 'w')
	for trigram in trigrams:
		fh.write(' '.join(trigram) + "\n")
	fh.close()
	fh = csv.writer(open(basedir + 'results/' + prefix + '-fdist.csv', 'w', encoding='utf-8'), dialect='excel')
	for word in fdist.keys():
		fh.writerow([word, fdist[word]])

def analyze_text(text):
	words = [w.lower() for w in text 
				if w not in string.punctuation 
				and w not in stopwords]
	b_finder = BigramCollocationFinder.from_words(words)
	t_finder = TrigramCollocationFinder.from_words(words)
	b_finder.apply_freq_filter(FREQ_FILTER)
	t_finder.apply_freq_filter(FREQ_FILTER)
	bigrams = b_finder.nbest(bigram_measures.pmi, TOT_NGRAMS)
	trigrams = t_finder.nbest(trigram_measures.pmi, TOT_NGRAMS)
	fdist = nltk.FreqDist(words)
	return(bigrams, trigrams, fdist)

# create diachronic results
for filename in wordlists.fileids():
	year = int(filename.partition(".")[0])	# grab the year from the filename
	bigrams, trigrams, fdist = analyze_text(wordlists.words(fileids=[filename]))
	write_results(bigrams, trigrams, fdist, str(year))

# create synchronic results
bigrams, trigrams, fdist = analyze_text(wordlists.words())
write_results(bigrams, trigrams, fdist, "all")

