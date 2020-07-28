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
	pos =  title.find("Segment")
	if pos <= 1:
		return "Bad format"
	return title[:pos-1]

def mergeSegment(infilename, outfilename):
	curStrain  = ""
	curSeq = ""
	curSeg = 10000
	outfile = open(outfilename, "w")
	genome =  0
	with open(infilename, "r") as infile:
		for line in infile.readlines():
			if line.startswith(">"):
				seg = getSegmentNo(line)
				if seg < 0:
					break
				if seg < curSeg:
					# a new strain
					strain = getStrainName(line)
					outfile.write(strain + "\n")
					genome += 1
					print(str(genome) + ": " + strain)
				else:
					# still the same strain: pad it with 32 N
					outfile.write("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN" + "\n")
				# set it as current segment
				curSeg = seg
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