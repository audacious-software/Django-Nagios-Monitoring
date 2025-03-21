#!/usr/bin/python

from __future__ import print_function

import argparse
import json
import sys

from urllib.request import urlopen

parser = argparse.ArgumentParser(description='Checks that no other issues are present.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urlopen(args.url) # nosec
data = json.load(response)

if data['issues']:
    print('OTHER ISSUES: %s' %','.join(data['issues']))
    sys.exit(2)

print('NO OTHER ISSUES')

sys.exit(0)
