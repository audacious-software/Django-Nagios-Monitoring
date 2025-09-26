#!/usr/bin/python

import argparse
import json
import sys

from urllib.request import urlopen

import six

parser = argparse.ArgumentParser(description='Checks that no other issues are present.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if data['issues']:
    six.print_('OTHER ISSUES: %s' %','.join(data['issues']))
    sys.exit(2)

six.print_('NO OTHER ISSUES')

sys.exit(0)
