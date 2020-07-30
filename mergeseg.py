#!/usr/bin/env python

#Usage: python mergeseg.py <input_fasta_file> <output_fasta_file>

import os, sys, getopt

def getSegmentNo(title):
	pos =  title.find("Segment")
	if pos < 0:
		return pos
	numchar = title[pos  + len("Segment") + 1]
	return int(numchar)

def getStrainName(title):
	segpos =  title.find("Segment")
	if segpos <= 1:
		return "Bad format"
	start =  title.find("|")
	return title[start+1:segpos-1]

def mergeSegment(infilename, outfilename):
	curStrain  = ""
	outfile = open(outfilename, "w")
	genome =  0
	with open(infilename, "r") as infile:
		for line in infile.readlines():
			if line.startswith(">"):
				strain = getStrainName(line)
				if strain != curStrain:
					# a new strain
					outfile.write(">" + strain + "\n")
					genome += 1
					print(str(genome) + ": " + strain)
				else:
					# still the same strain: pad it with 32 N
					outfile.write("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN" + "\n")
				# set it as current segment
				curStrain = strain
			else:
				if line != "\n":
					outfile.write(line)

	outfile.close()
	print("Processed all " + str(genome) + " strains")

def main():
	if len(sys.argv) < 3:
		print("Usage: python mergeseg.py <input_fasta_file> <output_fasta_file>")
		sys.exit()

	inputfile = sys.argv[1]
	outputfile = sys.argv[2]

	mergeSegment(inputfile, outputfile)

if __name__  == "__main__":
    main()