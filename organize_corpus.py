'''
For Cécile Alduy's Rhetoric of LePen project
Read in a series of CSV files with metadata describing corpus
Organize the full text files for processing

Mike Widner <mikewidner@stanford.edu>
'''
import os
import csv
import sys
import fileinput

from datetime import date
from shutil import copyfile
from collections import defaultdict

# list of files holding metadata about our texts
metadata = ['JMLP_discours.csv',
			'MLP_discours.csv',
			'JMLP_radio.csv',
			'JMLP_letters.csv',
			'MLP_radio.csv',
			'JMLP_tv.csv',
			'MLP_texte.csv',
			'MLP_tv.csv']
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
texts = basedir + 'corpora_unorganized/'
corpora = basedir + 'corpora/'

def main(): 
	''' Loop through metadata files; rename them all '''
	metadata_fh = open(basedir + 'filelist.csv', 'w')
	metadata_fh.write("author,genre,filename\n")
	years = defaultdict(list)
	authors = defaultdict(list)
	for filename in metadata:
		# print("Reading", filename)
		with open(basedir + "metadata/" + filename, 'r', encoding='utf-8') as fh:
			# try:
			reader = csv.DictReader(fh)
			# Columns: rid,filename,author,title,date,media,publication,place,length,collection,preparer
			for row in reader:
				# skip empties
				if len(row) == 0:
					continue
				path = os.path.dirname(row['filename'])
				filename = os.path.basename(row['filename'])
				# print("Processing", filename)
				# new_path = row['author'] + '/' + row['media']
				row['media'] = row['media'].strip()
				new_path = row["author"] + "/" + row["media"]
				if not os.path.isdir(new_path):
					os.makedirs(new_path)
				(day, month, year) = row['date'].split('/')
				date = row['date']
				year = date[-2:].strip()
				if len(year) == 1:
					year = "0" + year 	# hacky fix for messed up data
				if int(year) <= 99 and int(year) >= 80:
					year = "19" + year
				else:
					year = "20" + year
				author = row["author"]
				# living dangerously: could lead to filename collisions
				new_file = new_path + '/' + year + month + day + '.txt'
				# new_file = row["author"] + "-" + row['media'] + "-" + year + ".txt"
				years[year].append(corpora + new_file)
				authors[author].append(corpora + new_file)
				if not os.path.isdir(corpora + new_path):
					os.makedirs(corpora + new_path)
				# super kludgy
				try:
					# print(texts + row['filename'] + " -> " + corpora + new_file + "\n")
					metadata_fh.write(row["author"] + ',' + row['media'] + ',corpora/' + new_file + "\n")
					open(corpora + new_file, "w", encoding="utf-8").write(open(texts + row['filename'], encoding="MacRoman").read()) 
					# os.rename(, )
				except FileNotFoundError as err:
					print("Missing file: '" + row['filename'] + "'")
					years[year].remove(corpora + new_file)
					authors[author].remove(corpora + new_file)
				except UnicodeDecodeError as err:
					print(filename, err)
	metadata_fh.close()

	# print(years, authors)
	# Join all text from a single year into one file
	print("Grouping texts by year...")
	years_path = corpora + "years/"
	if not os.path.isdir(years_path):
		os.makedirs(years_path)
	for year in years:
		with open(years_path + year + ".txt", 'w') as fout:
			for filename in years[year]:
				with open(filename) as fin:
					for line in fin:
						fout.write(line)

	# Join all texts by an author
	print("Grouping texts by author...")
	authors_path = corpora + "authors/"
	if not os.path.isdir(authors_path):
		os.makedirs(authors_path)
	for author in authors:
		with open(authors_path + author + ".txt", 'w') as fout:
			for filename in authors[author]:
				with open(filename) as fin:
					for line in fin:
						fout.write(line)

if __name__ == '__main__':
	if sys.version_info[0] != 3:
	    print("This script requires Python 3")
	    exit(-1)
	main()