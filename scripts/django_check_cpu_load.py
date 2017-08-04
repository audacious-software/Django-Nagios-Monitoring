#!/usr/bin/python

import argparse
import json
import sys
import urllib2

CRITICAL_LOAD = 90
WARNING_LOAD = 75

parser = argparse.ArgumentParser(description='Checks CPU load on remote host.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urllib2.urlopen(args.url)
data = json.load(response)   

if 'cpu_percentage' in data:
    if data['cpu_percentage'] > CRITICAL_LOAD:
        print 'CPU LOAD CRITICAL: ' + str(data['cpu_percentage']) + '%'
        sys.exit(2)
    elif data['cpu_percentage'] > WARNING_LOAD:
        print 'CPU LOAD WARNING: ' + str(data['cpu_percentage']) + '%'
        sys.exit(1)
    else:
        print 'CPU LOAD OK: ' + str(data['cpu_percentage']) + '%'
        sys.exit(0)
else:
    print 'CPU LOAD UNKNOWN: ' + args.url
    sys.exit(3)
