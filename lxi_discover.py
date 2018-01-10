#!/usr/bin/env python
helpData = """
Date: 12 October 2017
Author:Srinivas N

Description: Finds all the LXI/VXI11 based instruments on the current subnet. The requirement for this tool arised
because there was this particular SORENSON power supply which had LAN LXI interface but NO interface to display
IP address assigned by DHCP. The LXI discover utility provided by LXI foundation was windows specific and required
lot of nonsense other softwares like apple bonjour file and printer services to be installed. So had to write an OS
independent light weight tool to get the Job done.

Usage: 1.Copy this script to a Linux or windows machine which is on the same network subnet as your device whose IP you need to find.
       2.Disconnect lan of your instrument and Run this script once.
       3.Reconnect Lan of your equipment and Rerun this script.
       4.Find your Device IP in the output list by comparing the two outputs.


Dependecy: This script uses a customised version of python-vxi11 package, which you should receive along with this script in same folder.
When running the binary executable we don't need to worry about it since it would be integrated into the executable.

"""

import vxi11
import time
import sys

discoverTimeout = 5#seconds
queryTimeout = 3#seconds

queryTimeout = 3#seconds

def queryInstr(Ip):
    try:
        vxi11.socket_timeout(queryTimeout)#uses customised vxi11 lib
        instr = vxi11.Instrument('TCPIP::'+Ip+'::INSTR')
        instr.timeout = queryTimeout-1 #this is required for some equipments, the vxi11 lib does +1 internally, and this is required for some instruments, need to find why
        instr.lock_timeout = queryTimeout-1
        queryString = str(instr.ask('*IDN?'))
        #print queryString
        instr.close()
        return queryString
    except vxi11.rpc.socket.timeout as timeout:
        #print str(timeout)
        return "Device not responding"
    except Exception as e:
        #print str(e)
        return queryString

def usage():
    print 'Usage: ./lxi_discovery <timeout_val_seconds> or ./lxi_discovery --help'

try:
    print 'LXI instrument Discovery Tool v1.2 by Srinivas N'
    if len(sys.argv) ==2:
        if sys.argv[1].isdigit() == True:
            discoverTimeout = int(sys.argv[1])
        elif sys.argv[1] == 'help' or sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print helpData+'\n'
            usage()
            sys.exit(0)
        else:
            print 'Invalid arguments given, Proceeding with default timeout value'
            usage()
    elif len(sys.argv) > 2:
        print 'Invalid arguments given, Proceeding with default timeout value'
        usage()
        
    print 'Please wait '+str(discoverTimeout)+' seconds, Discovering Instruments....\n'
    intrumentlist = vxi11.list_devices(timeout=discoverTimeout)

    for ip in intrumentlist:
        print ip+' : '+queryInstr(ip)
        time.sleep(0.1)
    print '\nLXI Instruments Discovery complete. If you did not find your instrument\nthen try increasing the timeout value and try again.'
    print 'Also sometimes devices are not detected properly when the computer/Laptop\nin which you are running this script is connected'
    print 'To network with WIFI instead of LAN. So it is recommended to connect LAN\nto your Computer/Laptop before running this Script/Program'
    print 'For help try ./lxi_discover -h'
    print 'press Enter to exit'
    raw_input()
    
except Exception as e:
    print 'There has been an exception, find the details below..'
    print str(e)
    print 'Please check if \"python-vxi11\" library is installed properly.'
    usage()
