#!/usr/bin/python

import argparse
import json
import sys

from urllib.request import urlopen

import six

CRITICAL = 90
WARNING = 75

parser = argparse.ArgumentParser(description='Checks CPU load on remote host.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if 'cpu_percentage' in data:
    if data['cpu_percentage'] > CRITICAL:
        six.print_('CPU LOAD CRITICAL: ' + str(data['cpu_percentage']) + '%')
        sys.exit(2)
    elif data['cpu_percentage'] > WARNING:
        six.print_('CPU LOAD WARNING: ' + str(data['cpu_percentage']) + '%')
        sys.exit(1)
    else:
        six.print_('CPU LOAD OK: ' + str(data['cpu_percentage']) + '%')
        sys.exit(0)
else:
    six.print_('CPU LOAD UNKNOWN: ' + args.url)
    sys.exit(3)
