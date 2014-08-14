#!/bin/sh

FILES=`ls results/ngrams/genre/*-bigram_prefix.csv`
CMD="python ngrams2graph.py"
for FILE in $FILES
	do
		CMD="$CMD -i $FILE "
	done
CMD="$CMD -o results/ngrams/genre/bigram_network.gexf"
eval $CMD