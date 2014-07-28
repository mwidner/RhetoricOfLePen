#!/bin/bash
FILES=/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/corpora*
for file in $FILES
  do /Applications/TreeTagger/cmd/tree-tagger-french-utf8 $file > /Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/tagged/$file.trt
done