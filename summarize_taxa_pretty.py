#!/usr/bin/env python

import argparse
import os
import csv
import json

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

def main():
	#  Argument Parser
	parser = argparse.ArgumentParser(description='Make pretty taxa summaries using D3')

	# Input file
	parser.add_argument('-i','--input',dest='input', help='The taxa summary folder created with summarize_taxa.py')
	# Output file
	parser.add_argument('-o','--output',dest='output', help='The output location')

	# Parse arguments
	args = parser.parse_args()
	indir = args.input
	outdir = args.output

	file_list = ['filtered_L1.txt','filtered_L2.txt', 'filtered_L3.txt', 'filtered_L4.txt', 'filtered_L5.txt', 'filtered_L6.txt', 'filtered_L7.txt']
	jsony = []
	for file in file_list:
		longfile =  "{}/{}".format(indir,file)
		if os.path.isfile(longfile):
			jsony.append(read_summary_file(longfile))
		else:
			jsony.append({'':''})
	print jsony[1][1]






if __name__ == '__main__':
	main()
