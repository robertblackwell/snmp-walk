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
from datetime import timedelta

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

def formatTimeInterval(time) :
	td = timedelta(seconds=time)
	return str(td)
	time_string = ""
	if time > 60 :
		seconds = time % 60
		time = time /60
		units = "minutes"
		time_string = str(seconds) + " seconds " + time_string
		if time > 60 :
			minutes = time % 60
			time = time / 60
			units = "hours"
			time_string = str(minutes) + " minutes " + time_string
			if time > 24 :
				hours = time % 24
				time = time / 24
				units = "days";
				time_string = str(hours) + " hours " + time_string
				if time > 7 :
					days = time % 7
					time = time / 7
					weeks = time
					units = "weeks"
					time_string = str(weeks) + " weeks " + str(days) + " days "  + time_string
				else :
					days = time % 7
					time_string = str(days) + " days "  + time_string
			else :
				hours = time % 24
				time_string = str(hours) + " hours " + time_string
		else :
			minutes = time % 60
			time_string = str(minutes) + " minutes " + time_string
	else :
		seconds = time % 60
		time_string = str(seconds) + " seconds " + time_string

	return time_string

def printFormattedResult(devName, mib, res):
	"""print the result in a single line with identification data (dev and mib) at the front to help location in log files"""	
	template = Template(" --> BGP Session $dev, Status: $status, Duration: $time ")

	units = "seconds"
	for index in [0,1]:
		entry = res[index]
		status = formatStatus(entry[0])
		time = entry[1]
		time_string = formatTimeInterval(time)
		output = devName + " " + mib + " " + template.substitute( dev=index, status = status, time=(time_string) )
		print output

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