#!/usr/bin/python

import argparse
import json
import sys
import urllib2

CRITICAL = 90
WARNING = 80

parser = argparse.ArgumentParser(description='Checks disk usage on remote host.')

parser.add_argument('url', help='URL of remote endpoint.')

args = parser.parse_args()

response = urllib2.urlopen(args.url) # nosec
data = json.load(response)   

max_percentage = 0
max_device = None

for device, percentage in data.iteritems():
    if percentage > max_percentage:
        max_percentage = percentage
        max_device = device

if max_device is None:
    print 'DISK UNKNOWN: ' + args.url
    sys.exit(3)
elif max_percentage >= CRITICAL:
    print 'DISK CRITICAL: ' + max_device + ', ' + str(max_percentage) + '%'
    sys.exit(2)
elif max_percentage >= WARNING:
    print 'DISK CRITICAL: ' + max_device + ', ' + str(max_percentage) + '%'
    sys.exit(2)
else:
    print 'DISK OK: ' + max_device + ', ' + str(max_percentage) + '%'
    sys.exit(0)
