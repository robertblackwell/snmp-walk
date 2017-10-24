#!/usr/bin/env python
#comment made by Richard
#
# This command processes the output from an snmpbulkwalk command to find the status and time in this status for the
# two embedded 'devices'. Prints the result on one line with identification data at the front so that the results can be easily
# found in log files
#
#	usage
#		cmd [options] nodeId mib fileName
#		
#			options
#				none
#				TODO - add option -x, prints output only if status is NOT
#						a GOOD status
#			arguments
#				nodeId, something like GM63702 
#				mib - identifies a data object within the node, something like
#						mib-2.15.3.1
#
import sys
import re
from string import Template

debug = False

def extractValueAfter(line, str):
	""" extract an integer value from the string line after the substring str"""
	if debug: print "extractValueAfter str:", str, " line:", line
	pos = line.find(str)
	if debug: print "extractValueAfter: pos: ", pos
	pend  = pos + len(str) 
	if debug: print "extractValueAfter: pend: ", pend
	if debug: print "extractValueAfter: line len: ", len(line)
	tail = line[pend: len(line)]
	tail = tail.strip()
	if debug: print "extractValueAfter: tail: ", tail
	return int(tail)

def p_usage():
	print "p_dor.py - process the output file from a snmpbulkwalk command to find non operational nodes"
	print "\nUsage :"
	print "\tp_dot.py dev_name mib fileName(optional)"
	print ""
	print "\tif fileName is not given will read from stdin"
	print ""
	
def verifyArgs(argv):
	"""check correct args and if necessary print usage message and exit"""
	if debug: print "verify args: ", len(argv)
	if (len(argv) != 4) and (len(argv) != 3) :
		p_usage()
		sys.exit()
		
def processFile(f, dev, mib):
	"""process file looking for two instances of a .2 object and two instances of a .16 object extract and return those"""
	mib_stripped = mib.replace("mib-","")
	dot2 = mib_stripped + ".2."
	dot16 = mib_stripped + ".16."

	dot2Values = []
	dot16Values = []

	for line in f:
		line = line.strip()
	# 	if debug : print(line);
		if dot2 in line :
			if debug: print "\tdot2", line
			value = extractValueAfter(line, "INTEGER:")
			dot2Values.append(value);
		elif dot16 in line :
			if debug: print "\tdot16", line
			value = extractValueAfter(line, "Gauge32:");
			dot16Values.append(value)

	assert len(dot2Values) == 2
	assert len(dot16Values) == 2
	res = []
	for indx in (0,1):
		tup = (dot2Values[indx], dot16Values[indx])
		res.append(tup)
	
	return res

def printRawResult(res):
	"""for debugging only - rpint raw result"""
	for entry in res:
		print "status: ", entry[0], " time: ", entry[1] ;

def formatStatus(rawStatus) :
	if rawStatus == 6 :
		return "UP(" + str(rawStatus) + ")"
	return "DOWN(" + str(rawStatus) + ")" 

def printFormattedResult(devName, mib, res):
	"""print the result in a single line with identification data (dev and mib) at the front to help location in log files"""	
	template = Template(" -->BGP Session $dev, Status: $status, Duration: $time $units")
	units = "seconds"
	for index in [0,1]:
		entry = res[index]
		units = "seconds"
		status = formatStatus(entry[0])
		time = entry[1]
		if entry[1] > 3600 :
			time = entry[1] / 3600
			units = "hours"
			if entry[1] / 3600 > 24 :
				units = "days";
				time = entry[1] / (3600*24)
				if (entry[1] / (3600 * 24)) > 7 :
					units = "weeks"
					time = entry[1] / (3600*24*7)
		output = devName + " " + template.substitute( dev=index, status = status, time=(time), units= units )
		print output
"""Richard entered this"""
def main():
	verifyArgs(sys.argv)
	
	# if file name not provided use stdin 	
	fileName = False
	if len(sys.argv) == 4:
		fileName = sys.argv[3]
		f = open(fileName);
	else:
		f = sys.stdin
		
	dev = sys.argv[1]
	mib = sys.argv[2]
	
	if debug:
		print "fileName", fileName
		print "dev", dev
		print "mib", mib 
	
	result = processFile(f, dev, mib)
	printFormattedResult(dev, mib, result)
	

if __name__ == "__main__":
	main()