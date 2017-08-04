#!/usr/bin/python

import argparse
import json
import sys
import urllib2

CRITICAL = 200
WARNING = 150

parser = argparse.ArgumentParser(description='Checks number of running processes on remote host.')

parser.add_argument('url', help='URL of remote endpoint.')

args = parser.parse_args()

response = urllib2.urlopen(args.url)
data = json.load(response)   

if 'count' in data:
    if data['count'] > CRITICAL:
        print 'PROCS CRITICAL: ' + str(data['count'])
        sys.exit(2)
    elif data['count'] > WARNING:
        print 'PROCS WARNING: ' + str(data['count'])
        sys.exit(1)
    else:
        print 'PROCS OK: ' + str(data['count'])
        sys.exit(0)
else:
    print 'PROCS UNKNOWN: ' + args.url
    sys.exit(3)
