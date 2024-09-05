# Parse symitar data and hopefully tell you all you need to know

import os
import sys

# GLOBAL VARIABLES
filePath = r"\\a\b\c\data.txt"
recordCounts = {}
relationships = {}
comboLine = ""

with open(filePath) as infile:
	for line in infile:
		# Ignore blank lines
		if line != "":
			# Builder for multiline records
			comboLine += line.rstrip()

			# Parser for single or complete comboLine
			if comboLine.rstrip().endswith('`'):
				# Add to or increase count for recordCounts dictionary for 3-Digit Symitar codes
				if comboLine[0:3] in recordCounts:
					recordCounts[comboLine[0:3]] += 1
				else:
					recordCounts[comboLine[0:3]] = 1
				
				# Split the comboLine for recordType and relationships
				bananaSplit = comboLine.replace('`','').split('~')
				recordType = bananaSplit[0]
				
				# Add recordType to relationships dictionary
				if recordType not in relationships:
					relationships[recordType] = []
				
				# Parse the comboLine for relationships
				for banana in bananaSplit[1:]:
					if banana[0:2] not in relationships.get(recordType):
						relationships[recordType].append(banana[0:2])
				
				# Reset comboLine as last operation in loop
				comboLine = ""

# show results
print("CODE : COUNT")
for key, value in sorted(recordCounts.items(), key=lambda x: x[0]):
	print("{}~ : {}".format(key, value))
print("\nCODE : RELATIONSHIPS")
for item in relationships.values():
	item.sort()
for key, value in sorted(relationships.items(), key=lambda x: x[0]):
	print("{}~ : {}".format(key, value))

#
#
#
#
#
#
#
#
#
#
