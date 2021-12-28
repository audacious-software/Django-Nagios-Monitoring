#!/usr/bin/python

from __future__ import print_function

from builtins import str # pylint: disable=redefined-builtin

import argparse
import json
import sys

import urllib2

CRITICAL = 350
WARNING = 300

parser = argparse.ArgumentParser(description='Checks number of running processes on remote host.')

parser.add_argument('url', help='URL of remote endpoint.')
parser.add_argument('--critical', help='Number of processes to trigger critical alert.', default=CRITICAL, type=int)
parser.add_argument('--warning', help='Number of processes to trigger warning alert.', default=WARNING, type=int)

args = parser.parse_args()

response = urllib2.urlopen(args.url) # nosec
data = json.load(response)

if 'count' in data:
    if data['count'] > args.critical:
        print('PROCS CRITICAL: ' + str(data['count']))
        sys.exit(2)
    elif data['count'] > args.warning:
        print('PROCS WARNING: ' + str(data['count']))
        sys.exit(1)
    else:
        print('PROCS OK: ' + str(data['count']))
        sys.exit(0)
else:
    print('PROCS UNKNOWN: ' + args.url)
    sys.exit(3)
