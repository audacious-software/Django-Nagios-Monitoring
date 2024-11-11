#!/usr/bin/python

from __future__ import print_function

from builtins import str # pylint: disable=redefined-builtin

import argparse
import json
import sys

from urllib.request import urlopen

CRITICAL = 5
WARNING = 2

parser = argparse.ArgumentParser(description='Checks logged in users on remote host.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if 'count' in data:
    if data['count'] > CRITICAL:
        print('USERS CRITICAL: ' + str(data['count']))
        sys.exit(2)
    elif data['count'] > WARNING:
        print('USERS WARNING: ' + str(data['count']))
        sys.exit(1)
    else:
        print('USERS OK: ' + str(data['count']))
        sys.exit(0)
else:
    print('USERS UNKNOWN: ' + args.url)
    sys.exit(3)
