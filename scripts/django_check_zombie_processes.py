#!/usr/bin/python

from builtins import str # pylint: disable=redefined-builtin

import argparse
import json
import sys

from urllib.request import urlopen

import six

CRITICAL = 5
WARNING = 1

parser = argparse.ArgumentParser(description='Checks number of zombie processes on remote host.')

parser.add_argument('url', help='URL of remote endpoint.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if 'count' in data:
    if data['count'] > CRITICAL:
        six.print_('PROCS CRITICAL: ' + str(data['count']))
        sys.exit(2)
    elif data['count'] > WARNING:
        six.print_('PROCS WARNING: ' + str(data['count']))
        sys.exit(1)
    else:
        six.print_('PROCS OK: ' + str(data['count']))
        sys.exit(0)
else:
    six.print_('PROCS UNKNOWN: ' + args.url)
    sys.exit(3)
