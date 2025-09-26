#!/usr/bin/python

import argparse
import json
import sys

from urllib.request import urlopen

import six

CRITICAL = 350
WARNING = 300

parser = argparse.ArgumentParser(description='Checks number of running processes on remote host.')

parser.add_argument('url', help='URL of remote endpoint.')
parser.add_argument('--critical', help='Number of processes to trigger critical alert.', default=CRITICAL, type=int)
parser.add_argument('--warning', help='Number of processes to trigger warning alert.', default=WARNING, type=int)

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if 'count' in data:
    if data['count'] > args.critical:
        six.print_('PROCS CRITICAL: ' + str(data['count']))
        sys.exit(2)
    elif data['count'] > args.warning:
        six.print_('PROCS WARNING: ' + str(data['count']))
        sys.exit(1)
    else:
        six.print_('PROCS OK: ' + str(data['count']))
        sys.exit(0)
else:
    six.print_('PROCS UNKNOWN: ' + args.url)
    sys.exit(3)
