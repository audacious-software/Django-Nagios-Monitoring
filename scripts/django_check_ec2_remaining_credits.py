#!/usr/bin/python

import argparse
import json
import sys

from urllib.request import urlopen

import six

CRITICAL = 0.25
WARNING = 0.5

parser = argparse.ArgumentParser(description='Checks EC2 credit balance load on remote host.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if 'credits_remaining' in data:
    if data['credits_remaining'] < CRITICAL:
        six.print_('EC2 CREDIT BALANCE CRITICAL: %.3f / %.3f' % (data.get('latest_balance', 0), data.get('maximum_observed', 0)))
        sys.exit(2)
    elif data['credits_remaining'] < WARNING:
        six.print_('EC2 CREDIT BALANCE WARNING: %.3f / %.3f' % (data.get('latest_balance', 0), data.get('maximum_observed', 0)))
        sys.exit(1)
    else:
        six.print_('EC2 CREDIT BALANCE OK: %.3f / %.3f' % (data.get('latest_balance', 0), data.get('maximum_observed', 0)))
        sys.exit(0)
else:
    six.print_('EC2 CREDIT BALANCE UNKNOWN: ' + args.url)
    sys.exit(3)
