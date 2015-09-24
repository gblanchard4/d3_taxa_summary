#!/usr/bin/env python

import argparse
import os
import csv
import json
import glob

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Make pretty taxa summaries
'''
# Need to format the filtered tables
def read_summary_file(taxa_file):
	# Filename
	level = taxa_file.lstrip('filtered_').rstrip('.txt')
	dict_list = []
	with open(taxa_file, 'r') as validfile:
		fieldnames = ""
		for line in validfile:
			# Grab header
			if line.startswith('#'):
				fieldnames = line.lstrip('#').rstrip('\n').split('\t')
			else:
				format_line = line.strip('\n').split('\t')
				dict_list.append(dict(zip(header, format_line)))
	return dict_list

# File summary
def read_taxa_files(file_list, category, outdir):
	for file in file_list:
		level = os.path.basename(file).split('_L')[1].rstrip('.txt')
		with open(file, 'r') as handle, open(outdir+'/'+level+'.txt', 'w') as outlevel:
			for line in handle:
				if line .startswith('#'):
					header = line.lstrip('#').rstrip('\n').replace(';','-').replace('[','').replace(']','').split('\t')
					category_pos = header.index(category)
					taxa_pos = header.index("Description")+1
					outlevel.write(header[category_pos]+','+','.join(map(str,header[taxa_pos:]))+'\n')
				else:
					clean_line =  line.rstrip('\n').split('\t')
					outlevel.write(clean_line[category_pos]+','+','.join(map(str,clean_line[taxa_pos:]))+'\n')





def main():
	#  Argument Parser
	parser = argparse.ArgumentParser(description='Make pretty taxa summaries using D3')

	# Input file
	parser.add_argument('-i','--input',dest='input', help='The taxa summary folder created with summarize_taxa.py', required=True)
	# Output file
	parser.add_argument('-o','--output',dest='output', help='The output location', required=True)
	# Category
	parser.add_argument('-c','--category', dest='category', help='The category to summarize the taxa by', required=True)

	# Parse arguments
	args = parser.parse_args()
	indir = args.input
	outdir = args.output
	category = args.category

	if not os.path.exists(outdir):
		os.makedirs(outdir)

	file_list = sorted(glob.glob("{}/*_L*.txt".format(indir)))
	print file_list

	read_taxa_files(file_list, category, outdir)






	# file_list = ['filtered_L1.txt','filtered_L2.txt', 'filtered_L3.txt', 'filtered_L4.txt', 'filtered_L5.txt', 'filtered_L6.txt', 'filtered_L7.txt']
	# jsony = []
	# for file in file_list:
	# 	longfile =  "{}/{}".format(indir,file)
	# 	if os.path.isfile(longfile):
	# 		jsony.append(read_summary_file(longfile))
	# 	else:
	# 		jsony.append({'':''})
	# print jsony[1][1]






if __name__ == '__main__':
	main()
