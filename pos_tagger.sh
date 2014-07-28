#!/bin/sh

POS_PATH="/Applications/StanfordNLP/stanford-postagger-full-2014-01-04"
JAVA="/usr/bin/java"
DOC_PATH="/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/corpora/years"
FILES=`ls ${DOC_PATH}/*.txt`
TT_FR="/Applications/TreeTagger/cmd/tagger-chunker-french"
RESULTS_DIR="/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/results/treetagger"

for FILE in ${FILES}
	do
		FILENAME=`echo $FILE | /usr/bin/awk -F. '{ print $1 }'`
		# $JAVA -mx300m -classpath ${POS_PATH}/stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model ${POS_PATH}/models/french.tagger -outputFormat xml -textFile $FILE > ${FILENAME}.xml
		/bin/cat ${FILE} | $TT_FR > ${FILENAME}.sgml
	done