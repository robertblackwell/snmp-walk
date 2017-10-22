#!/bin/bash

SECONDS=0

COUNT=`cat ./$1 | wc -l`

#where to log
TIMESTAMP="$(/bin/date +%Y-%m-%d.%H:%M:%S)"
LOGFILE="./bgp_check_Results_$TIMESTAMP.log"

#proof its working
printf 'Working...\n\n'

#ping devices on list
cat ./$1 | xargs -P 100 -n 1 /home/rblackwe/scripts/bgpcheck_gun > $LOGFILE 
echo ""

#display results of all devices are were not reachable
echo "---------------------"
echo "Down BGP sessions"
echo "---------------------"
grep 2 $LOGFILE
echo ""

#display totals
#TOTUP=`grep up $LOGFILE | wc -l`
#TOTDN=`grep down $LOGFILE | wc -l`
#echo "---------------------"
#echo Total Devices: $COUNT
#echo Total up:     $TOTUP - $(($TOTUP * 100 / $COUNT))%
#echo Total down:   $TOTDN - $(($TOTDN * 100 / $COUNT))%
#echo "---------------------"
#echo ""

#display how much time has passed
duration=$SECONDS
echo "Time Elapsed: $(($duration / 60))m $(($duration % 60))s"
echo ""
echo "Completed! - $LOGFILE"
echo ""
