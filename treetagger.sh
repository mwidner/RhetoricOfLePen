#!/bin/bash
FILES=/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/corpora/authors/*
for file in $FILES
  do /Applications/TreeTagger/cmd/tree-tagger-french $file > /Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/tagged/$file.txt
done