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
CS_RO=@u_6*G4s.

snmpbulkwalk -v2c -c $CS_RO ${DEV} ${MIB} | ./p_dot.py ${DEV} ${MIB_STRIPPED}

