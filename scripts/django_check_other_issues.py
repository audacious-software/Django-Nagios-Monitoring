#!/usr/bin/python

import argparse
import json
import sys
import urllib2

parser = argparse.ArgumentParser(description='Checks that no other issues are present.')

parser.add_argument('url', help='URL of remote endpoint to check.')

args = parser.parse_args()

response = urllib2.urlopen(args.url) # nosec
data = json.load(response)

if data['issues']:
    print 'OTHER ISSUES: ' + ','.join(data['issues'])
    sys.exit(2)

print 'NO OTHER ISSUES'

sys.exit(0)
