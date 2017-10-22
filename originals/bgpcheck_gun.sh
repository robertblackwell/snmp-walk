#!/bin/bash

  #performing SNMPwalk and process the output
  snmpbulkwalk -v2c -c @u_6*G4s. $1 mib-2.15.3.1 | ./p_dot.py 
  # or
#  snmpbulkwalk -v2c -c @u_6*G4s. $1 mib-2.15.3.1 | ./p_dot.sh 
