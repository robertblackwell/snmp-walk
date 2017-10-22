#!/bin/bash
###
## This script processes the output from a command of the form
## 
## 	snmpbulkwalk -v2c -c @u_6*G4s. gm63702 mib-2.15.3.1 > log
## 	
## 	Usage for post processing the obove command is:
## 	
## 	./p_dot.sh ./log gm63702 2.15.3.1 > processed_log
## 	
## 	The processed log file will consts of a single line that begins with the text
## 	
## 	gm63702 mib-2.15.3.1 .....
## 	
## 	An error in one  of the devices of interest will be signalled by the inclusion
## 	of the text "NOTOK" somewhere in the output line
##
## 	The intention that this script will be part of a larger script that is
## 	fired off by xargs to process a group of devices in parallel
## 	
##If you only want a report of failures then run
##
## 	./p_dot.sh ./log gm63702 2.15.3.1 | grep "NOTOK "> processed_log
##
##
## You can test this with
## 
## ./p_dot.sh bulk.temp gm63702 "2.15.3.1"
##
GM=$2
MID=$3
DOT2=${MID}.2.
DOT16=${MID}.16.
DOT2_V=()
INPUT=$1

# cat $1 | fgrep "mib-2\.15\.3\.1\.2\." | sed s/^.*INTEGER:\s//g

function dot2 {
	TMP2=./dot2${RANDOM}
	index=0
	a=("y" "y")
	cat $1 | fgrep ${DOT2} | sed s/^.*INTEGER:.//g > ${TMP2} 

	while read line
	do
		# echo "index ${index} this is the line [" $line "]"
		a[$index]=$line
		index=$(expr $index + 1)
	done < ${TMP2}
	rm -rf ${TMP2}
	DOT2_V=("${a[@]}")
}

function dot16 {
	index=0
	a=("z" "z")
	TMP16=./dot16${RANDOM}
	cat $1 | fgrep ${DOT16} | sed s/^.*Gauge32:.//g > $TMP16
	while read line
	do
		# echo "index ${index} this is the line [" $line "]"
		let " line = line / (3600)" ## convert to hours
		a[$index]=$line
		index=$(expr $index + 1)
	done < ${TMP16}
	rm -rf ${TMP16}
	DOT16_V=("${a[@]}")
}


function testOK {
	dev=$1
	status=${DOT2_V[$dev]}
	hrs=${DOT16_V[$dev]}
	# echo testOK $1 $dev $status $hrs

	if [ ${DOT2_V[$1]} != "6x" ]; then
		echo $device $1 is NOTOK has been in this state for ${DOT16_V[$1]} hours
		# result= "${result} device ${dev} is NOTOK has been in this state for ${hrs} hours"
	else
		echo device $1 is OK
		# result="${result} device" ${dev} "is OK"
	fi 
}

dot2 $INPUT
dot16 $INPUT
res1=$(testOK 0) 
res2=$(testOK 1)
echo "$GM mib-$MID -- $res1 -- $res2"

