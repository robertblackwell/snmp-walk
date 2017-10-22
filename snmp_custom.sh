#
# This is the script that xargs shoud call 
# you will need an input file for xargs that the following contents made up fo lines like
# 
# gm63702 2.15.3.1
# 
# and the xargs call will need option -n 2
#

DEV=$1
MIB_STRIPPED=2.15.3.1
MIB=mib-${MIB_STRIPPED}

snmpbulkwalk -v2c -c @u_6*G4s. ${1} ${MIB} | ./p_dot.py ${1} ${MIB_STRIPPED}

