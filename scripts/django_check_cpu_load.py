#!/usr/bin/python

from __future__ import print_function

from builtins import str  # pylint: disable=redefined-builtin

import argparse
import json
import sys

import urllib.request, urllib.error, urllib.parse

CRITICAL = 90
WARNING = 75

parser = argparse.ArgumentParser(description='Checks CPU load on remote host.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urllib.request.urlopen(args.url) # nosec
data = json.load(response)   

if 'cpu_percentage' in data:
    if data['cpu_percentage'] > CRITICAL:
        print('CPU LOAD CRITICAL: ' + str(data['cpu_percentage']) + '%')
        sys.exit(2)
    elif data['cpu_percentage'] > WARNING:
        print('CPU LOAD WARNING: ' + str(data['cpu_percentage']) + '%')
        sys.exit(1)
    else:
        print('CPU LOAD OK: ' + str(data['cpu_percentage']) + '%')
        sys.exit(0)
else:
    print('CPU LOAD UNKNOWN: ' + args.url)
    sys.exit(3)
