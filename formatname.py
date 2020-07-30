#!/usr/bin/env python

#Usage: python formatname.py <input_fasta_file> <output_fasta_file>

import os, sys, getopt

def getSegmentNo(title):
	pos =  title.find("Segment")
	if pos < 0:
		return pos
	numchar = title[pos  + len("Segment") + 1]
	return int(numchar)

def getHA(title):
	pos =  title.find("Subtype:")
	if pos < 0:
		return pos

	hpos = title.find("H", pos)
	if hpos < 0:
		return hpos

	npos =  title.find("N", hpos)
	if npos < 0:
		return npos

	return int(title[hpos+1:npos])

def getNA(title):
	pos =  title.find("Subtype:")
	if pos < 0:
		return pos

	hpos = title.find("H", pos)
	if hpos < 0:
		return hpos

	npos =  title.find("N", hpos)
	if npos < 0:
		return npos

	breaknpos =  title.find("|", npos)
	if breaknpos < 0:
		return breaknpos

	return int(title[npos+1:breaknpos])

def getStrainName(title):
	segpos =  title.find("Name")
	if segpos <= 1:
		return "Bad format"
	return title[1:segpos-1]

def formatName(infilename, outfilename):
	outfile = open(outfilename, "w")
	genome =  0
	with open(infilename, "r") as infile:
		for line in infile.readlines():
			if line.startswith(">"):
				strain = getStrainName(line)
				seg = getSegmentNo(line)
				strHN = ""
				if seg == 4:
					if line.find("Subtype:mixed") > 0:
						strHN = "Hemagglutinin type: mixed | from: "
					else:
						HA = getHA(line)
						strHN = "Hemagglutinin type: H" + str(HA) + " | from: "
				elif seg == 6:
					if line.find("Subtype:mixed") > 0:
						strHN = "Neuraminidase type: mixed | from: "
					else:
						NA = getNA(line)
						strHN = "Neuraminidase type: N" + str(NA) + " | from: "

				outfile.write(">" + strHN + strain + "\n")
				genome += 1
				print(str(genome) + ": " + strain)
			else:
				if line != "\n":
					outfile.write(line)

	outfile.close()
	print("Processed all " + str(genome) + " strains")

def main():
	if len(sys.argv) < 3:
		print("Usage: python formatname.py <input_fasta_file> <output_fasta_file>")
		sys.exit()

	inputfile = sys.argv[1]
	outputfile = sys.argv[2]

	formatName(inputfile, outputfile)

if __name__  == "__main__":
    main()