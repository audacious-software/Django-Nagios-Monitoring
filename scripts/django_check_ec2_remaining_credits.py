#!/usr/bin/python

from __future__ import print_function

from builtins import str  # pylint: disable=redefined-builtin

import argparse
import json
import sys

import urllib2

CRITICAL = 0.25
WARNING = 0.5

parser = argparse.ArgumentParser(description='Checks EC2 credit balance load on remote host.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urllib2.urlopen(args.url) # nosec
data = json.load(response)   

if 'credits_remaining' in data:
    if data['credits_remaining'] < CRITICAL:
        print('CPU CREDIT BALANCE CRITICAL: %.3f / %.3f' % (data.get('latest_balance', 0), data.get('maximum_observed', 0)))
        sys.exit(2)
    elif data['cpu_percentage'] < WARNING:
        print('CPU CREDIT BALANCE WARNING: %.3f / %.3f' % (data.get('latest_balance', 0), data.get('maximum_observed', 0)))
        sys.exit(1)
    else:
        print('CPU CREDIT BALANCE OK: %.3f / %.3f' % (data.get('latest_balance', 0), data.get('maximum_observed', 0)))
        sys.exit(0)
else:
    print('CPU CREDIT BALANCE UNKNOWN: ' + args.url)
    sys.exit(3)
