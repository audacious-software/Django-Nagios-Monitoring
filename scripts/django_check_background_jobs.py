#!/usr/bin/python

import argparse
import json
import sys

from urllib.request import urlopen

import six

parser = argparse.ArgumentParser(description='Checks that background jobs are running in a timely fashion.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if data['errors']:
    six.print_('OVERDUE BACKGROUND JOBS: ' + ','.join(data['errors']))
    sys.exit(2)

if data['warnings']:
    six.print_('OVERDUE BACKGROUND JOBS: ' + ','.join(data['warnings']))
    sys.exit(1)

six.print_('BACKGROUND JOBS OK')
sys.exit(0)
