#!/usr/bin/python

from __future__ import print_function

import argparse
import json
import sys

import urllib2

parser = argparse.ArgumentParser(description='Checks that background jobs are running in a timely fashion.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urllib2.urlopen(args.url) # nosec
data = json.load(response)

if data['errors']:
    print('OVERDUE BACKGROUND JOBS: ' + ','.join(data['errors']))
    sys.exit(2)

if data['warnings']:
    print('OVERDUE BACKGROUND JOBS: ' + ','.join(data['warnings']))
    sys.exit(1)

print('BACKGROUND JOBS OK')
sys.exit(0)
