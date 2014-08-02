#!/bin/sh

DOC_PATH="/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/corpora/authors"
FILES=`ls ${DOC_PATH}/*.txt`
TT_FR="/Applications/TreeTagger/cmd/tagger-chunker-french"
RESULTS_DIR="/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/results/treetagger/authors"

if [ ! -d $RESULTS_DIR ];
	then
		mkdir -p $RESULTS_DIR
fi

for FILE in ${FILES}
	do
		FILENAME=`echo $FILE | /usr/bin/awk 'BEGIN{FS="/"}{print $NF}'`
		/bin/cat ${FILE} | $TT_FR > ${RESULTS_DIR}/tagged_${FILENAME}
	done