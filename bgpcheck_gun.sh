#!/bin/bash
#performing SNMPwalk
echo "got arg 1 = " $1
#snmpbulkwalk -v2c -c @u_6*G4s. $1 1.3.6.1.2.1.15.3.1.2 